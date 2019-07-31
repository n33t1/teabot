from flask import Flask
from flask_restful import Api

from db import db
from src.resources.event import Event
from src.resources.action import Action

import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')

logger = logging.getLogger()
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Event, '/event')
api.add_resource(Action, '/action')

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=3000, debug=True)
