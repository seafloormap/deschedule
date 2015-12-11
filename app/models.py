from app import db, timezone

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
    
    time   = db.Column(db.Time)
    length = db.Column(db.Interval, default = datetime.timedelta(minutes = 75))

    monday    = db.Column(db.Boolean(), default=False)
    tuesday   = db.Column(db.Boolean(), default=False)
    wednesday = db.Column(db.Boolean(), default=False)
    thursday  = db.Column(db.Boolean(), default=False)
    friday    = db.Column(db.Boolean(), default=False)
    saturday  = db.Column(db.Boolean(), default=False)
    sunday    = db.Column(db.Boolean(), default=False)

    instructor = db.Column(db.String(32), nullable = True)
    email      = db.Column(db.String(32), nullable = True)
    room       = db.Column(db.String(32), nullable = True)

    def __init__(self, class_code, number, kind, time, days, instructor=None,
            email=None, room=None, length=75):
        self.class_code = class_code
        self.number     = number
        self.kind       = kind

        if type(time) == str:
            self.time = datetime.datetime.strptime(time, '%H:%M').time()
        else:
            self.time = time

        if type(length) == int:
            self.length = datetime.timedelta(minutes=length)
        else:
            self.length = length

        self.monday    = 'Monday'    in days or 'mon' in days
        self.tuesday   = 'Tuesday'   in days or 'tue' in days
        self.wednesday = 'Wednesday' in days or 'wed' in days
        self.thursday  = 'Thursday'  in days or 'thu' in days
        self.friday    = 'Friday'    in days or 'fri' in days
        self.saturday  = 'Saturday'  in days or 'sat' in days
        self.sunday    = 'Sunday'    in days or 'sun' in days

        self.instructor = instructor
        self.email      = email
        self.room       = room

    def __repr__(self):
        return "<Section '{} {} {}'>".format(
                self.class_code, self.kind, self.number)

    def __json__(self):
        return {'instructor': self.instructor,
                'email': self.email,
                'class_code': self.class_code,
                'number': self.number,
                'kind': self.kind,
                'days': self.days(),
                'time': self.time.replace(tzinfo=timezone.UMBC_TZINFO),
                'room': self.room
            }

    def days(self, brief=False):
        l = filter(lambda x: x != None, [
                'Monday'    if self.monday    else None,
                'Tuesday'   if self.tuesday   else None,
                'Wednesday' if self.wednesday else None,
                'Thursday'  if self.thursday  else None,
                'Friday'    if self.friday    else None,
                'Saturday'  if self.saturday  else None,
                'Sunday'    if self.sunday    else None])
        if brief:
            return map(lambda day: day[:3].lower(), l)
        else:
            return l

    def on_weekday(self, date):
        """Return true if the section is scheduled to meet on a given day,
        using only the Weekday to check."""
        # Check if the weekday matches the output from days()
        return date.strftime("%A") in self.days()

    def events(self):
        for day in self.semester.days():
            if not self.on_weekday(day): continue
            event = {
                'summary': '{} {}'.format(self.class_code, self.kind),
                'dtstart': datetime.datetime.combine(day,
                    self.time.replace(tzinfo=timezone.UMBC_TZINFO)),
                'duration': self.length,
            }
            if self.instructor or self.email:
                event['organizer'] = '{} <{}>'.format(
                        self.instructor if self.instructor else '',
                        self.email if self.email else '')
            if self.room:
                event['location'] = self.room

            yield event
