from app import app, db
from app.models import *
from app.renderers import *

import flask
from flask import request
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import BrowsableAPIRenderer

import functools

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

# Endpoint for browsing all listed semesters.
@app.route('/api/umbc/semester/')
@api_response
def api_all_semesters():
    semesters = Semester.query.all()
    return semesters

@app.route('/api/umbc/semester/<semester>/', methods=['GET'])
@api_response
def api_semester(semester):
    semester = semester.upper()
    s = Semester.query.filter(Semester.name == semester).one_or_none()

    return s

# Create a new semester listing.
@app.route('/api/umbc/semester/<semester>/', methods=['POST'])
@api_response
def api_new_semester(semester):
    s = Semester(
            name  = semester,
            start = request.form['start'],
            end   = request.form['end']
    )
    db.session.add(s)
    db.session.commit()
    app.logger.info('Created semester "{}"'.format(s))
    return None

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
    section = Section(
        class_code = class_code,
        number = section_number,
        kind = request.form['kind'],
        days = request.form['days'].split('/'),
        time = request.form['time'],
        length = int(request.form['length']) \
                if 'length' in request.form else None,
        instructor = request.form['instructor'] \
                if 'instructor' in request.form else None,
        email = request.form['email'] \
                if 'email' in request.form else None,
        room = request.form['room'] \
                if 'room' in request.form else None
    )
    print(section)
    s.sections.append(section)
    db.session.add(s)
    db.session.add(section)
    db.session.commit()
    app.logger.info('Created section "{}"'.format(section))
    return None

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
@set_renderers(ExtendedJSONRenderer, BrowsableAPIRenderer, ICalendarRenderer)
@api_response
def api_section_events(semester, class_code, section_number):
    """List calendar events for a particular section of a class."""
    section = Section.query.join(Semester) \
            .filter(Semester.name == semester.upper()) \
            .filter(db.and_(Section.class_code == class_code,
                            Section.number == section_number)).one()
    return section.events()
