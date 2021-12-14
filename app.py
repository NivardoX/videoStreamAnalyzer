import json

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import RABBIT_MQ_URL, DATABSE_DEFAULT_URL, DATABSE_URL


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=f'pyamqp://{RABBIT_MQ_URL}//',
        include=['consumer.tasks']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
flask_app.config['SQLALCHEMY_DATABASE_URI'] = DATABSE_URL
flask_app.config['SECRET_KEY'] = 'your secret key'


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)
celery = make_celery(flask_app)

from api.controllers import *
