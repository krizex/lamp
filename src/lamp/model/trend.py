from lamp.model import db


class Trend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(32))
    start_price= db.Column(db.Float, nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float, nullable=False)
    cur_hold = db.Column(db.Integer, nullable=False)
    own = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return 'Trend <Code %r>' % self.code
