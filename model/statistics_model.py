from db import db

class StatisticModel(db.Model):
    
    __tablename__ = "statustics"
    _id = db.Column(db.Integer, primary_key=True)
    id_joke = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    
    def __init__(self, id_joke, rate):
        self.id_joke = id_joke
        self.rate = rate
        
    def json(self):
        return {
            "id" : self.id,
            "id_joke" : self.id_joke,
            "rate" : self.rate
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def get_id_joke_static(cls, _id):
        return cls.filter_by(id_joke=_id).first()