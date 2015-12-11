from app import db

import datetime

def public_dict(o, exclude=('_',)):
    return {k: v for k, v in o.__class__.__dict__.items()
            if not (k.startswith(exclude) or hasattr(v, '__call__'))}

schedule_sections = db.Table('schedule_sections',
        db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id')),
        db.Column('section_id', db.Integer, db.ForeignKey('section.id')),
)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sections = db.relationship("Section", secondary=schedule_sections)

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    start  = db.Column(db.Date)
    end    = db.Column(db.Date)
    breaks = db.relationship("Break", backref = 'semester', lazy = 'joined')

    def __init__(self, name, start, end, breaks=[]):
        if type(start) == str:
            start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        if type(end) == str:
            end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        self.name = name.upper()
        self.start = start
        self.end = end
        self.breaks = [Break(*r) for r in breaks]

    def __repr__(self):
        return "<Semester '{}'>".format(self.name)

    def __json__(self):
        return {'name': self.name,
                'start': str(self.start),
                'end': str(self.end),
                'breaks': self.breaks
            }

    def days(self):
        day = self.start
        while day <= self.end:
            if all((day not in b for b in self.breaks)):
                yield day
            day += datetime.timedelta(days=1)

class Break(db.Model):
    __table_args__ = (
            db.UniqueConstraint('name', 'semester_id',
                name='_name_semester_uc'),
        )
    id    = db.Column(db.Integer, primary_key = True)

    start = db.Column(db.Date)
    end   = db.Column(db.Date)

    name = db.Column(db.String(32), nullable = True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, start, end=None, name=None):
        if type(start) == str:
            start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        if type(end) == str:
            end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

        self.start = start
        self.end = end if end != None else start

        self.name = name

    def __contains__(self, date):
        return self.start <= date and date <= self.end

    def __repr__(self):
        rangefmt = '{} to {}'.format(self.start, self.end) \
                if self.start != self.end \
                else '{}'.format(self.start)

        return "<Break '{}' {}>".format(self.name, rangefmt)

    def __json__(self):
        return {'start': self.start,
                'end': self.end,
                'name': self.name
            }

class Section(db.Model):
    __table_args__ = (
            db.UniqueConstraint('class_code', 'number', 'semester_id',
                name='_class_section_num_uc'),
        )
    id = db.Column(db.Integer, primary_key=True)

    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    semester = db.relationship('Semester', backref='sections')

    class_code = db.Column(db.String(16))
    number     = db.Column(db.Integer)
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

    def __init__(self, class_code, number, kind, time, days, instructor=None,
            email=None):
        self.class_code = class_code
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

