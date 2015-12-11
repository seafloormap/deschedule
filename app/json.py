import flask
from flask.ext.api.renderers import JSONRenderer

import datetime

class ExtendedJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        try:
            return o.__json__()
        except AttributeError:
            pass
        if hasattr(o, '__iter__'):
            return list(o)
        if o.__class__ == datetime.date:
            return o.strftime('%Y-%m-%d')
        if o.__class__ == datetime.time:
            return o.strftime('%H:%M:%S')

        return super().default(o)

class ExtendedJSONRenderer(JSONRenderer):
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
