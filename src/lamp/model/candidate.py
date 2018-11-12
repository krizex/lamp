from lamp.model import db

class Candidate(db.Model):
    code = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(32))
    start_pe = db.Column(db.Float, nullable=False)
    stop_pe = db.Column(db.Float, nullable=False)
    start_price = db.Column(db.Float, nullable=False)
    own = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __init__(self, code, name, start_pe, stop_pe, start_price, own, note):
        self.code = code
        self.name = name
        self.start_pe = start_pe
        self.stop_pe = stop_pe
        self.start_price = start_price
        self.own = own
        self.note = note

    def __repr__(self):
        return '<Code %r>' % self.code

    def update(self, d):
        self.name = d['name']
        self.start_pe = d['start_pe']
        self.stop_pe = d['stop_pe']
        self.start_price = d['start_price']
        self.own = d['own']
        self.note = d['note']
