from app import app, db
from app.models import *
from app.renderers import *

import flask
from flask import request
from flask.ext.api.decorators import set_renderers

from sqlalchemy.exc import DBAPIError
import sqlalchemy.sql.expression

import functools, itertools

def api_response(f):
    @functools.wraps(f)
    def func_wrapper(*args, **kwargs):
        resp = f(*args, **kwargs)
        if type(resp) != dict or 'data' not in resp:
            return {'data': resp}
        else:
            return resp
    return func_wrapper

def api_wrap(return_values, status='ok'):
    return {'status': status, 'data': return_values}

## API Endpoints
#
# At present, all API endpoints begin with /api/umbc/ because we may some day
# support multiple schools.
@app.route('/api/')
@api_response
def api_root():
    """All of the functionality of Deschedule is provided by the API. The documentation is
    sparse, but can be found in the source code at
    https://github.com/alexander-bauer/deschedule/blob/master/app/api.py"""
    return None

# Endpoint for browsing all listed semesters.
@app.route('/api/umbc/semester/')
@api_response
def api_all_semesters():
    semesters = Semester.query.order_by(sqlalchemy.desc('end')).all();
    return semesters

# Create a new semester listing.
@app.route('/api/umbc/semester/<semester>', methods=['POST'])
@api_response
def api_new_semester(semester):
    s = Semester(
            name  = semester,
            start = request.data.get('start'),
            end   = request.data.get('end')
    )
    db.session.add(s)
    db.session.commit()
    app.logger.info('Created semester "{}"'.format(s))
    return None

@app.route('/api/umbc/semester/<semester>/', methods=['GET'])
@api_response
def api_semester(semester):
    semester = semester.upper()
    s = Semester.query.filter(Semester.name == semester).one_or_none()

    return s

@app.route('/api/umbc/semester/<semester>/schedule/')
@api_response
def api_schedule(semester):
    """Build a per-session schedule using the `sections` URL parameter. It must
    be formatted similarly to `sections=CODE100.01,CODE110.04`, which would
    select the class CODE100 section 1 and CODE110 section 4."""
    # Get the pairs of class codes and section numbers.
    section_pairs = [tuple(pair.split('.')) for pair in
            request.args.get('sections').split(',')]

    try:
        sections = Section.query.join(Semester) \
                .filter(Semester.name == semester.upper()) \
                .filter(db.tuple_(Section.class_code, Section.number)\
                    .in_(section_pairs)).all()
    except DBAPIError:
        app.logger.info("DB Backend does not support compound key 'IN' queries, \
reverting to composed 'OR/AND' query.")
        # Because the backend does not support in_ for tuples, we abuse *args
        # and list comprehensions to create a subsitute query.
        sections = Section.query.join(Semester) \
                .filter(Semester.name == semester.upper()) \
                .filter(db.or_(
                    *tuple((db.and_(
                        Section.class_code == code, Section.number == number)
                        for code, number in section_pairs)))) \
                .all()

    return sections

@app.route('/api/umbc/semester/<semester>/schedule/events/')
@set_renderers(ExtendedJSONRenderer, MyBrowsableAPIRenderer, ICalendarRenderer)
@api_response
def api_schedule_events(semester):
    """Build a per-session schedule just like the above endpoint, but also
    generate all events. Also can generate iCalendar format output."""
    # Get the pairs of class codes and section numbers.
    section_pairs = [tuple(pair.split('.')) for pair in
            request.args.get('sections').split(',')]

    try:
        sections = Section.query.join(Semester) \
                .filter(Semester.name == semester.upper()) \
                .filter(db.tuple_(Section.class_code, Section.number)\
                    .in_(section_pairs)).all()
    except DBAPIError:
        app.logger.info("DB Backend does not support compound key 'IN' queries, \
reverting to composed 'OR/AND' query.")
        # Because the backend does not support in_ for tuples, we abuse *args
        # and list comprehensions to create a subsitute query.
        sections = Section.query.join(Semester) \
                .filter(Semester.name == semester.upper()) \
                .filter(db.or_(
                    *tuple((db.and_(
                        Section.class_code == code, Section.number == number)
                        for code, number in section_pairs)))) \
                .all()

    return itertools.chain(*(section.events() for section in sections))

@app.route('/api/umbc/semester/<semester>/days/')
@api_response
def api_semester_days(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return s.days()

@app.route('/api/umbc/semester/<semester>/break', methods=['POST'])
@api_response
def api_new_break(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    b = Break(
        name  = request.form['name'],
        start = request.form['start'],
        end   = request.form['end']
    )
    s.breaks.append(b)
    db.session.add(s)
    db.session.add(b)
    db.session.commit()
    app.logger.info('Created break "{}"'.format(b))
    return None

@app.route('/api/umbc/semester/<semester>/break/', methods=['GET'])
@api_response
def api_all_breaks(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return s.breaks

@app.route('/api/umbc/semester/<semester>/search/<classes>', methods=['GET'])
@api_response
def api_search(semester, classes):
    class_codes = classes.upper().split(',')
    print(class_codes)
    sections = Section.query.join(Semester)\
            .filter(Semester.name == semester.upper())\
            .filter(Section.class_code.in_(class_codes))\
            .order_by(Section.class_code)\
            .order_by(Section.number)\
            .all()
    return sections

@app.route('/api/umbc/semester/<semester>/class/')
@api_response
def api_all_classes(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return s.sections

@app.route('/api/umbc/semester/<semester>/class/<class_code>/')
@api_response
def api_class_sections(semester, class_code):
    """List all sections for the class code in the semester."""
    sections = Section.query.join(Semester)\
            .filter(Semester.name == semester.upper())\
            .filter(Section.class_code == class_code)\
            .order_by(Section.number)\
            .all()
    return sections

@app.route('/api/umbc/semester/<semester>/class/<class_code>/<int:section_number>',
        methods=['POST'])
@api_response
def api_new_section(semester, class_code, section_number):
    """Create a new section attached to the Semester. Days are given as
    'mon/tue/wed/thu/fri/sat/sun' or any combination thereof."""
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    if request.data.get('kind') not in Section.kinds:
        flask.abort(400)

    section = Section(
        class_code = class_code,
        number = section_number,
        kind = request.data.get('kind'),
        days = request.data.get('days').split('/'),
        time = request.data.get('time'),
        length = int(request.data.get('length', 75)),
        instructor = request.data.get('instructor', None),
        email = request.data.get('email', None),
        room = request.data.get('room', None)
    )
    s.sections.append(section)
    db.session.add(s)
    db.session.add(section)
    db.session.commit()
    app.logger.info('Created section "{}"'.format(section))
    return section

@app.route('/api/umbc/semester/<semester>/class/<class_code>/<int:section_number>/')
@api_response
def api_section(semester, class_code, section_number):
    section = Section.query.join(Semester) \
            .filter(Semester.name == semester.upper()) \
            .filter(db.and_(Section.class_code == class_code,
                            Section.number == section_number)).one()
    print(section)
    return section

@app.route('/api/umbc/semester/<semester>/class/<class_code>/<int:section_number>/events/')
@set_renderers(ExtendedJSONRenderer, MyBrowsableAPIRenderer, ICalendarRenderer)
@api_response
def api_section_events(semester, class_code, section_number):
    """List calendar events for a particular section of a class."""
    section = Section.query.join(Semester) \
            .filter(Semester.name == semester.upper()) \
            .filter(db.and_(Section.class_code == class_code,
                            Section.number == section_number)).one()
    return section.events()

@app.route('/api/umbc/semester/<semester>/random/')
@api_response
def api_random_section(semester):
    """Return a number of random sections from the given semester."""
    number = request.data.get('number', 5)
    s = Section.query.join(Semester) \
            .filter(Semester.name == semester.upper()) \
            .order_by(sqlalchemy.sql.expression.func.random()) \
            .limit(number);
    return s;
