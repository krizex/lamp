from lamp.model import db

class Grid(db.Model):
    code = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(32))
    high= db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    own = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __init__(self, code, name, high, low, size, width, own, note):
        self.code = code
        self.name = name
        self.high = high
        self.low = low
        self.size = size
        self.width = width
        self.own = own
        self.note = note

    def __repr__(self):
        return '<Code %r>' % self.code

    def update(self, d):
        self.name = d['name']
        self.high = d['high']
        self.low = d['low']
        self.size = d['size']
        self.width = d['width']
        self.own = d['own']
        self.note = d['note']
