from sqlalchemy import Column, Integer, String
from app.db import Base

class WordModel(Base):
    __tablename__ = "word"
    id = Column(Integer, primary_key=True)
    word = Column(String(20))
    len_word = Column(Integer)
    
    def __init__(self, word, len_word):
        self.word = word
        self.len_word = len_word
        
    def json(self):
        return {'id': self.id, "word":self.word, "len_word": self.len_word}
    
    @classmethod
    def find_by_word(cls, word):
        return cls.query.filter_by(word=word).first()
    
    
    def save_to_db(self):
        self.session.add(self)
        self.session.commit()
    