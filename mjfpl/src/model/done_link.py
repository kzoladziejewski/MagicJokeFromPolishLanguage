try:
    from db import db
except ModuleNotFoundError:
    from mjfpl.src.db import db


class DoneLink(db.Model):
    __tablename__ = "link"
    _id = db.Column(db.Integer, primary_key=True)
    done_link = db.Column(db.String(160))

    def json(self):
        return {
            "id": self._id,
            "done_link": self.done_link,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_url_link(cls, url):
        return cls.query.filter_by(done_link=url).first()
