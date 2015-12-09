from app import db

import datetime

schedule_breaks = db.Table('schedule_breaks',
        db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id')),
        db.Column('break_id', db.Integer, db.ForeignKey('break.id')),
)

schedule_sections = db.Table('schedule_sections',
        db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id')),
        db.Column('section_id', db.Integer, db.ForeignKey('section.id')),
)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    start = db.Date()
    end   = db.Date()
    
    breaks = db.relationship("Break", secondary=schedule_breaks)

    sections = db.relationship("Section", secondary=schedule_sections)

class Break(db.Model):
    id    = db.Column(db.Integer, primary_key = True)
    start = db.Date()
    end   = db.Column(db.Date, nullable = True)

    def __contains__(self, date):
        if end != None:
            return start <= date and date <= end
        else:
            return start == date

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    department = db.Column(db.String(8))
    number     = db.Column(db.Integer())
    kind       = db.Column(db.Enum("Lecture", "Laboratory", "Discussion"))
    
    time      = db.Column(db.Time)
    monday    = db.Column(db.Boolean(), default=False)
    tuesday   = db.Column(db.Boolean(), default=False)
    wednesday = db.Column(db.Boolean(), default=False)
    thursday  = db.Column(db.Boolean(), default=False)
    friday    = db.Column(db.Boolean(), default=False)
    saturday  = db.Column(db.Boolean(), default=False)
    sunday    = db.Column(db.Boolean(), default=False)

    instructor = db.Column(db.String(32), nullable = True)
    email      = db.Column(db.String(32), nullable = True)

    def __init__(self, department, number, kind, time, days, instructor=None,
            email=None):
        self.department = department
        self.number     = number
        self.kind       = kind

        if type(time) == str:
            self.time = datetime.datetime.strptime(time, '%H:%M').time()
        else:
            self.time = time

        self.monday    = 'mon' in days
        self.tuesday   = 'tue' in days
        self.wednesday = 'wed' in days
        self.thursday  = 'thu' in days
        self.friday    = 'fri' in days
        self.saturday  = 'sat' in days
        self.sunday    = 'sun' in days

        self.instructor = instructor
        self.email      = email

    def __repr__(self):
        return "<Section '{} {} {}' '{}'>".format(
                self.department, self.number, self.kind,
                '/'.join(filter(lambda x: x != None,
                    ['mon' if self.monday else None,
                     'tue' if self.tuesday else None,
                     'wed' if self.wednesday else None,
                     'thu' if self.thursday else None,
                     'fri' if self.friday else None,
                     'sat' if self.saturday else None,
                     'sun' if self.sunday else None])))

