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
@app.route('/api/umbc/semester/<semester>', methods=['POST'])
def api_new_semester(semester):
    s = Semester(
            name  = semester,
            start = request.form['start'],
            end   = request.form['end']
    )
    db.session.add(s)
    db.session.commit()
    app.logger.info('Created semester "{}"'.format(s))
    return {'status': 'successful'}

@app.route('/api/umbc/semester/<semester>/<class_id>/<int:section_number>')
def api_section(semester, class_id, section_number):
    semester = semester.upper()
    class_id = class_id.upper()
    return {'semester': semester,
            'class': class_id,
            'section_number': section_number
    }
