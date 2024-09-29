from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # lecturer, tutor, ta