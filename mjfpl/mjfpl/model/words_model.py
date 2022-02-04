from mjfpl.db import db

class WordsModel(db.Model):
    __tablename__ = "words"
    _id = db.Column(db.Integer, primary_key=True)
    nouns = db.Column(db.String(80))
    url = db.Column(db.String(80))
    genitive = db.Column(db.String(80))
    len_word = db.Column(db.Integer)

    def __init__(self, nouns, url, genitive, lew_word ):
        self.nouns = nouns
        self.url = url
        self.genitive = genitive
        self.len_word = lew_word

    def json(self):
        return {
            "id" : self._id,
            "url": self.url,
            "nouns": self.nouns,
            "genitive": self.genitive,
            "len_word": self.len_word
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

