from flask import Flask
from flask_restful import Api

from db import db
from app.read_all_data_from_wikipedia import FindAllWords
from resource.create_jokes import CreateJokeResource
from resource.jokes import JokeResource
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///magicjokefrompolishlanguage.db'
api = Api(app)

api.add_resource(CreateJokeResource, "/create_joke_resource")
api.add_resource(JokeResource, "/joke")


@app.before_first_request
def create_tables():
    # db.create_all()
    # faw = FindAllWords()
    # faw.get_all_next_page(0)
    # faw.get_all_hyperlink_to_details_of_nouns()
    # faw.add_nouns_to_database()
    pass

if __name__ == "__main__":
    # host = "80.211.195.240"
    # port = 80
    host = "192.168.100.4"
    port = 8080
    db.init_app(app)
    app.run(host, port, debug=True)