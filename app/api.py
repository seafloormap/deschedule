from app import app, db
from app.models import *

import flask
from flask import request

def dict_wrap(return_values, status='ok'):
    return {'status': status, 'data': return_values}

## API Endpoints
#
# At present, all API endpoints begin with /api/umbc/ because we may some day
# support multiple schools.

# Endpoint for browsing all listed semesters.
@app.route('/api/umbc/semester/')
def api_all_semesters():
    semesters = Semester.query.all()
    return dict_wrap(semesters)

@app.route('/api/umbc/semester/<semester>/', methods=['GET'])
def api_semester(semester):
    semester = semester.upper()
    s = Semester.query.filter(Semester.name == semester).one_or_none()

    # It is necessary to return a dictionary, for some reason, so try to JSON
    # encode.
    return dict_wrap(s)

# Create a new semester listing.
@app.route('/api/umbc/semester/<semester>/', methods=['POST'])
def api_new_semester(semester):
    s = Semester(
            name  = semester,
            start = request.form['start'],
            end   = request.form['end']
    )
    db.session.add(s)
    db.session.commit()
    app.logger.info('Created semester "{}"'.format(s))
    return dict_wrap(None)

@app.route('/api/umbc/semester/<semester>/days/')
def api_semester_days(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return dict_wrap(s.days())

@app.route('/api/umbc/semester/<semester>/break/', methods=['GET'])
def api_all_breaks(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return dict_wrap(s.breaks)

@app.route('/api/umbc/semester/<semester>/break/', methods=['POST'])
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
    return dict_wrap(None)

@app.route('/api/umbc/semester/<semester>/class/')
def api_all_classes(semester):
    s = Semester.query.filter(Semester.name == semester.upper()).one()
    return dict_wrap(s.sections)

@app.route('/api/umbc/semester/<semester>/class/<class_code>/<int:section_number>',
        methods=['POST'])
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
    return dict_wrap(None)
