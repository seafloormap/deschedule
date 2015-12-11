from app import app, db, models

from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer

@app.route('/')
@app.route('/index')
@set_renderers(HTMLRenderer)
def index():
    return 'Hello, world.'

@app.route('/api/umbc/semester/')
def api_semester():
    semesters = models.Semester.query.all()
    return {'semesters': semesters}

@app.route('/api/umbc/semester/<semester>/<class_id>/<int:section_number>')
def api_section(semester, class_id, section_number):
    semester = semester.upper()
    class_id = class_id.upper()
    return {'semester': semester,
            'class': class_id,
            'section_number': section_number
    }
