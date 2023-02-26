from db import db

class CommentsModel(db.Model):
    __tablename__ = "comments"
    _id = db.Column(db.Integer, primary_key=True)
    id_joke = db.Column(db.Integer)
    comment = db.Column(db.String(3600))
    
    def __init__(self, id_joke, comment):
        self.id_joke = id_joke
        self.comment = comment
        
    def json(self):
        return {
            "id" : self._id,
            "id_joke" : self.id_joke,
            "comment" : self.comment
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, _id):
        return cls.query.filter_by(id_joke=_id).all()