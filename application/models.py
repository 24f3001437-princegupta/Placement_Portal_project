from .database import db
class User(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    username= db.Column(db.String(), unique=True, nullable=False)
    password= db.Column(db.String(), nullable=False)
    role= db.Column(db.String(),nullable=False)
    student_profile = db.relationship('Student', backref='user_account', uselist=False)
    company_profile = db.relationship('Company', backref='user_account', uselist=False)

class Student(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_info= db.Column(db.String(),unique= True,nullable=False)
    resume= db.Column(db.String())
    department = db.Column(db.String())
    is_blacklisted= db.Column(db.Boolean(), default=False) 
    full_name= db.Column(db.String(), nullable=False)        

class Company(db.Model):
    id= db.Column(db.Integer(),primary_key=True)
    user_id= db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=False)
    company_name= db.Column(db.String(),nullable=False ,unique= True)
    hr_contact= db.Column(db.String(),nullable=False)
    is_approved= db.Column(db.Boolean(),default=False)
    is_blacklisted= db.Column(db.Boolean(), default=False)

class PlacementDrive(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id'), nullable=False)
    drive_name = db.Column(db.String(100), nullable=False)
    eligibility = db.Column(db.String(), nullable=True)
    job_title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    deadline = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), default='Pending')

class Application(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer(), db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(), default='Applied')
