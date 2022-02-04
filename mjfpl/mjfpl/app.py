from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db

from mjfpl.resource.jokes import JokeResource
from mjfpl.resource.create_jokes import CreateJokeResource
from mjfpl.resource.statistic import StatisticResource
from mjfpl.resource.hello_world import HelloWorld
from mjfpl.application.read_all_data_from_wikipedia import FindAllWords

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///magicjokefrompolishlanguage.db'
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(CreateJokeResource, "/create_joke_resource")
api.add_resource(JokeResource, "/joke")
api.add_resource(StatisticResource, "/static")
api.add_resource(HelloWorld, "/")

@app.before_first_request
def create_tables():
    print("???")
    db.create_all()
    db.session.commit()

    faw = FindAllWords()

    # if not jk:
    #     faw = FindAllWords()
    #     faw.get_all_next_page()
    #     faw.get_all_hyperlink_to_details_of_nouns()
    #     faw.add_nouns_to_database()

if __name__ == "__main__":
    # host = "80.211.195.240"
    # port = 80
    host = "192.168.100.4"
    # host = "0.0.0.0"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=False)