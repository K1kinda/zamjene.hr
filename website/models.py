from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

    school = db.relationship('School', backref=db.backref('users', lazy=True))
    classroom = db.relationship('Classroom', backref=db.backref('users', lazy=True))


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login_password = db.Column(db.String(100), nullable=False)


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    school = db.relationship('School', backref=db.backref('classrooms', lazy=True))


class Zamjene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    zamjena = db.Column(db.String(100), nullable=False)


class RasporedSati(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    raspored_string = db.Column(db.String(1000), nullable=False)


class RasporedUcionica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    raspored_string = db.Column(db.String(10000), nullable=False)


class Obavjesti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)