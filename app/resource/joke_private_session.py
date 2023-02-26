from http import HTTPStatus

from flask_restful import Resource, reqparse
try:
    from model import JokeModel, WordsModel
except:
    from app.model import JokeModel, WordsModel
    
class JokePrivateSession(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('joke', type=str, required=True)
    parser.add_argument('answer', type=str, required=True)
    
    def get(self):
        words = WordsModel.find_all_word()      
        # words = requests.get(url='http://127.0.0.1:8080/word')
        for word in words:
            noun = word.json().get("nouns")
            if len(noun) > 1:
                for element in range(1, len(noun)):
                    gen_first = WordsModel.find_genitive(noun[element:])
                    if gen_first:
                        gen = gen_first.json().get("genitive")
                        joke = f"Jak jest {noun} bez {gen}"
                        if not JokeModel.find_skip_repeated_joke(joke):
                            JokeModel(joke, noun[0])
        return {'msg' : 'Jokes added'}, HTTPStatus.OK
    
    def post(self):
        data = self.parser.parse_args()
        if not JokeModel.find_skip_repeated_joke(data.get('joke')):
            JokeModel(data.get('joke'),data.get('answer'))
            return {"msg": 'Joke added'}, HTTPStatus.OK
        return {'msg' : 'Joke exist in database'}, HTTPStatus.CONFLICT