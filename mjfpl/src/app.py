from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db

from resources import JokeResource, CreateJokeResource, StatisticResource, HelloWorld
from application.read_all_data_from_wikipedia import FindAllWords

import logging
import datetime

from  pathlib import Path
logging.basicConfig(filename = f'flask_log_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log', level=logging.INFO, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

app = Flask(__name__)
CORS(app)
path_to_database = Path(__file__).parent.joinpath('instance').joinpath('mjfpl.db').resolve()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+str(path_to_database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(CreateJokeResource, "/create_joke_resource")
api.add_resource(JokeResource, "/joke")
api.add_resource(StatisticResource, "/static")
api.add_resource(HelloWorld, "/")

def find_word():
    faw = FindAllWords()
    faw.get_all_next_page()
    faw.get_all_hyperlink_to_details_of_nouns()
    faw.add_nouns_to_database()

if __name__ == "__main__":
    # host = "80.211.195.240"
    # port = 80
    # host = "localhost"
    host = "0.0.0.0"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=False)