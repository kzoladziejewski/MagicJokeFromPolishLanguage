from http import HTTPStatus

from flask_restful import Resource, reqparse
try:
    from model import WordsModel
except:
    from app.model import WordsModel
    
class WordResource(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument("nouns",type=str,required=True)
    parser.add_argument("url",type=str,required=True)
    parser.add_argument("genitive",type=str,required=True)
    parser.add_argument("len_word",type=str,required=True)
    
    def get(self):
        return {'msg': WordsModel.find_all_word()}, HTTPStatus.OK
    
    def post(self):
        data = self.parser.parse_args()
        if not WordsModel.find_nouns(data.get('nouns')):
            WordsModel(data.get('nouns'), data.get('url'), data.get('genitive'), data.get('len_word')).save_to_db()
            return {'msg' : 'Added word'}, HTTPStatus.ACCEPTED
        return {'msg' : 'Word exist in database'}, HTTPStatus.CONFLICT