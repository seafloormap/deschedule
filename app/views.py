from app import app, db, models

import flask
from flask import request
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer

@app.route('/')
@app.route('/index')
@set_renderers(HTMLRenderer)
def index():
    return 'Hello, world.'
