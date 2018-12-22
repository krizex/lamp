from lamp.model import db

class Grid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(32))
    high= db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    own = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return '<Code %r>' % self.code

