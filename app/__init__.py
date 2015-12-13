from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

from app import renderers
app.config['DEFAULT_RENDERERS'] = [
        'app.renderers.ExtendedJSONRenderer',
        'app.renderers.MyBrowsableAPIRenderer'
]

app.config.from_object('config')
db = SQLAlchemy(app)

from app import api
from app import views, models
