from lamp.model import db

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(32))
    start_pe = db.Column(db.Float, nullable=False)
    stop_pe = db.Column(db.Float, nullable=False)
    start_price = db.Column(db.Float, nullable=False)
    own = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return '<Code %r>' % self.code

