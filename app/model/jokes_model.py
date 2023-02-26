try:
    from db import db
except:
    from app.db import db

class JokeModel(db.Model):
    __tablename__ = "jokes"
    _id = db.Column(db.Integer, primary_key=True)
    joke_question = db.Column(db.String(160))
    joke_answer = db.Column(db.String(2))
    rate = db.Column(db.Integer)

    def __init__(self, joke_question, joke_answer, rate=0):
        self.joke_answer = joke_answer
        self.joke_question = joke_question
        self.rate = rate

    def json(self):
        return {
            "id" : self._id,
            "joke_question": self.joke_question,
            "joke_answer": self.joke_answer,
            'rate' : self.rate
        }

    @classmethod
    def find_all_jokes(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_skip_repeated_joke(cls, joke):
        return cls.query.filter_by(joke_question=joke).first()

    @classmethod
    def get_first_joke(cls):
        return cls.query.filter_by(_id=1).first()