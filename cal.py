import icalendar
import datetime

ICAL_PRODID = 'https://github.com/AlexanderBauer/deschedule'
ICAL_VERSION = '2.0'

JSON_DATEF = '%Y-%m-%d'
JSON_TIMEF = '%H:%M'
JSON_WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

class Semester:
    def __init__(self, start, end, classes, breaks=[], holidays=[]):
        self.start = start
        self.end   = end

        self.classes = classes

        self.breaks = breaks
        self.holidays = holidays

    # Generate datetime.date for each day in a semester, including weekends, but
    # not breaks or holidays.
    def days(self):
        i = self.start
        while i < self.end:
            if i not in self.breaks and i not in self.holidays: yield i
            i += datetime.timedelta(days=1)

    def class_instances(self):
        return {class_name: class_o.section_instances(self.days())
                for class_name, class_o in self.classes.items()}

    def calendar(self):
        cal = icalendar.Calendar()
        cal.add('prodid', ICAL_PRODID)
        cal.add('version', ICAL_VERSION)

        for class_name, sections in self.class_instances().items():
            for section_type, time_pairs in sections.items():
                for start, length in time_pairs:
                    ev = icalendar.Event()
                    ev.add('summary', '{} {}'.format(class_name, section_type))
                    ev.add('dtstart', start)
                    ev.add('duration', length)
                    cal.add_component(ev)

        return cal

    @classmethod
    def from_json_dict(cls, d):
        args = d
        args['start']   = datetime.datetime.strptime(d['start'],
                JSON_DATEF).date()
        args['end']   = datetime.datetime.strptime(d['end'],
                JSON_DATEF).date()
        args['classes'] = {name: Class.from_json_dict(properties) for name,
                   properties in d['classes'].items()}
        return cls(**args)

class Class:
    def __init__(self, sections):
        self.sections = sections

    def section_instances(self, days):
        return {section_name: map(section.time_duration, filter(section.on_day, days))
                for section_name, section in self.sections.items()}

    @classmethod
    def from_json_dict(cls, d):
        args = d
        args['sections'] = {kind: Section.from_json_dict(properties)
                for kind, properties in d['sections'].items()}
        return cls(**args)

class Section:
    def __init__(self, days, time, length):
        self.days   = days
        self.time   = time
        self.length = length

    def on_day(self, date):
        return date.weekday() in self.days

    def time_duration(self, date):
        return (datetime.datetime.combine(date, self.time), self.length)

    @classmethod
    def from_json_dict(cls, d):
        args = d
        args['days']   = [JSON_WEEKDAYS.index(day) for day in d['days']]
        args['time']   = datetime.datetime.strptime(d['time'], JSON_TIMEF).time()
        args['length'] = datetime.timedelta(minutes=d['length'])
        return cls(**args)
