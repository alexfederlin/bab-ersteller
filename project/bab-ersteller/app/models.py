from app import db

class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    reports = db.relationship('Report', backref='plane', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plane_id = db.Column(db.Integer, db.ForeignKey('plane.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tasks = db.relationship('Task', backref='report', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lfd_nr = db.Column(db.Integer, nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    task_description = db.Column(db.String(500), nullable=False)  # Renamed field
    fix_description = db.Column(db.String(500), nullable=False)
    reference = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    executor = db.Column(db.String(100), nullable=False)

