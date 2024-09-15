import logging
import datetime

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db
from pathlib import Path
from resources import JokeResource, CreateJokeResource, StatisticResource, HelloWorld
from constant import PATH_TO_DATABASE
from application import FindAllWords

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

class DataKeeper():
    faw = FindAllWords()
    client_is_runned = False

data_keeper = DataKeeper()

@app.route('/create_db')
def before_first_request():
    if not Path(PATH_TO_DATABASE).is_file():
        db.create_all()
    return {'200': "DB created"}

@app.route('/find_words')
def find_words():
    if not data_keeper.client_is_runned:
        data_keeper.client_is_runned = True
        data_keeper.faw.get_all_next_page()
        data_keeper.faw.get_all_hyperlink_to_details_of_nouns()
        data_keeper.faw.get_all_nouns_from_link()
        data_keeper.client_is_runned = False
    return {"200":"Client started"}

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=False)
