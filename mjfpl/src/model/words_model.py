try:
    from db import db
except ModuleNotFoundError:
    from mjfpl.src.db import db


class WordsModel(db.Model):
    __tablename__ = "words"
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80))
    len_word = db.Column(db.Integer)
    mianownik = db.Column(db.String(80))
    dopelniacz = db.Column(db.String(80))
    celownik = db.Column(db.String(80))
    biernik = db.Column(db.String(80))
    narzednik = db.Column(db.String(80))
    miejscownik = db.Column(db.String(80))
    wolacz = db.Column(db.String(80))
    plural = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def json(self):
        return {
            self.__dict__
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_word(cls):
        return cls.query.all()

    @classmethod
    def find_genitive(cls, word):
        return cls.query.filter_by(genitive=word).first()
