import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db
from pathlib import Path
from resources import JokeResource, CreateJokeResource, StatisticResource, HelloWorld
from constant import PATH_TO_DATABASE
from application.read_all_data_from_wikipedia import FindAllWords
import logging
import datetime


logging.basicConfig(filename=f'flask_log_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log',
                    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(PATH_TO_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(CreateJokeResource, "/create_joke_resource")
api.add_resource(JokeResource, "/joke")
api.add_resource(StatisticResource, "/static")
api.add_resource(HelloWorld, "/")
@app.route('/create_db')
def before_first_request():
    if not Path(PATH_TO_DATABASE).is_file():
        db.create_all()
    return {'200': "DB created"}

@app.route('/find_words')
def find_words():
    faw = FindAllWords()
    faw.get_all_next_page()
    faw.get_all_hyperlink_to_details_of_nouns()
    faw.get_all_nouns_from_link()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=False)
