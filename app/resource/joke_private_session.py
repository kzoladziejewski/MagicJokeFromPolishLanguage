from http import HTTPStatus

from flask_restful import Resource, reqparse
try:
    from model import JokeModel
except:
    from app.model import JokeModel
    
class JokePrivateSession(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('joke', type=str, required=True)
    parser.add_argument('answer', type=str, required=True)
    
    def post(self):
        data = self.parser.parse_args()
        if not JokeModel.find_skip_repeated_joke(data.get('joke')):
            JokeModel(data.get('joke'),data.get('answer'))
            return {"msg": 'Joke added'}, HTTPStatus.OK
        return {'msg' : 'Joke exist in database'}, HTTPStatus.CONFLICT