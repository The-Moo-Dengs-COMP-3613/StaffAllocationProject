from App.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(100), nullable=False, unique=True)
    courseName = db.Column(db.String(100), nullable=False)
    
    # Foreign keys linking to the Staff table
    lecturer_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    ta_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    
    # Relationships with the Staff table
    lecturer = db.relationship('Staff', foreign_keys=[lecturer_id])
    tutor = db.relationship('Staff', foreign_keys=[tutor_id])
    ta = db.relationship('Staff', foreign_keys=[ta_id])
