from http import HTTPStatus

from flask_restful import Resource, reqparse
from flask_cors import cross_origin
try:
    from model import CommentsModel
except:
    from app.model import CommentsModel

class CommentsResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("id", type=int, required=True, help="Id of joke")
    parser.add_argument("comment", type=int, required=True, help="New comment")


    @cross_origin()
    def post(self):
        data = self.parser.parse_args()
        id_joke = data.get('id')
        comment = data.get('comment')
        CommentsModel(id_joke, comment).save_to_db()
        return {'msg' : "Comment added"}, HTTPStatus.ACCEPTED