from lamp.model import db


class Rebound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(32))
    days = db.Column(db.Integer, nullable=False, default=11)
    ratio = db.Column(db.Float, nullable=False, default=0.05)
    note = db.Column(db.Text)

    def __repr__(self):
        return 'Rebound <Code %r>' % self.code
