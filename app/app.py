from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db

import logging
import datetime

from resource.jokes import JokeResource
from pathlib import Path
database_path = Path(__file__).parent.parent.joinpath('mjfpl.db')
logging.basicConfig(filename=f'flask_log_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log',
                    level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(JokeResource, "/joke")


@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=False)
