from flask_restful import Resource
from model.jokes_model import  JokeModel
from random import choice

class JokeResource(Resource):

    def get(self):
        jokes = JokeModel.find_all_jokes()

        return_joke = choice(jokes)
        return return_joke.json()

