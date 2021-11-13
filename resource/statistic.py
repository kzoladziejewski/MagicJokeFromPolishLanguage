from model.statistics_model import StatisticModel
from flask_restful import Resource, reqparse
from model.jokes_model import JokeModel
from http import HTTPStatus
from flask_cors import cross_origin

class StatisticResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("id", type=int, required=True, help="Id of joke")
    parser.add_argument("vote", type=int, required=True, help="Voke id")

    @cross_origin()
    def post(self):
        data = self.parser.parse_args()
        
        id_joke = data.get('id')
        rate_joke = data.get("vote")
        if rate_joke > 0:
            rate_joke = 1
        elif rate_joke < 0:
            rate_joke = -1
        static_joke = StatisticModel.get_id_joke_static(id_joke)
        if not static_joke:
            rate = 0 + rate_joke
            StatisticModel(id_joke, rate=rate).save_to_db()
            return {HTTPStatus.OK, {"msg" : "Added"}}
        static = StatisticModel.get_id_joke_static(id_joke)
        rate = int(static.json().get("rate"))
        static.rate = rate + rate_joke
        static.save_to_db()
        return {HTTPStatus.OK, {"msg" : {"Rate updated"}}}
