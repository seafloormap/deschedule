import datetime

DSTSTART = datetime.datetime(1, 4, 1, 2)
DSTEND = datetime.datetime(1, 10, 25, 1)

def first_sunday_on_or_after(dt):
    days_to_go = 6 - dt.weekday()
    return dt + (datetime.timedelta(days=1) * days_to_go)

class USTimeZone(datetime.tzinfo):
    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = datetime.timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return datetime.timedelta(0)
        assert dt.tzinfo is self

        # Find first Sunday in April & the last in October.
        start = first_sunday_on_or_after(DSTSTART.replace(year=dt.year))
        end = first_sunday_on_or_after(DSTEND.replace(year=dt.year))

        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        if start <= dt.replace(tzinfo=None) < end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

UMBC_TZINFO = USTimeZone(-5, 'Eastern', 'EST', 'EDT')
