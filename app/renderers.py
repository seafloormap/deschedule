import flask
from flask.ext.api import renderers

import datetime
import icalendar

class ExtendedJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        try:
            return o.__json__()
        except AttributeError:
            pass
        if hasattr(o, '__iter__'):
            return list(o)
        if o.__class__ == datetime.datetime:
            return o.strftime('%a, %d %b %Y %H:%M %Z')
        if o.__class__ == datetime.date:
            return o.strftime('%Y-%m-%d')
        if o.__class__ == datetime.time:
            return o.strftime('%H:%M %Z')
        if o.__class__ == datetime.timedelta:
            return str(o)

        return super().default(o)

class ExtendedJSONRenderer(renderers.JSONRenderer):
    def render(self, data, media_type, **options):
        # Requested indentation may be set in the Accept header.
        try:
            indent = max(min(int(media_type.params['indent']), 8), 0)
        except (KeyError, ValueError, TypeError):
            indent = None
        # Indent may be set explicitly, eg when rendered by the browsable API.
        indent = options.get('indent', indent)
        return flask.json.dumps(data,
                cls=ExtendedJSONEncoder,
                ensure_ascii=False,
                indent=indent)

class MyBrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    template = 'api_base.html'

class ICalendarRenderer(renderers.BaseRenderer):
    """Render an iterable collection of dictionaries in iCalendar format."""
    media_type = 'text/calendar'

    def render(self, data, media_type, **options):
        # Data must be an iterable collection of dictionaries.
        cal = icalendar.Calendar()
        cal.add('prodid', 'https://github.com/alexander-bauer/deschedule')
        cal.add('version', '2.0')
        for event_dict in data['data']:
            event = icalendar.Event()
            for key, value in event_dict.items():
                event.add(key, value)
            cal.add_component(event)

        return cal.to_ical()
