#!/usr/bin/env python3

import cal
import datetime
import json

s = cal.Semester.from_json_dict(
    json.loads('''{
    "start":   "2016-01-25",
    "end":     "2016-05-10",
    "classes": {
        "ABCD 101": {
            "sections": {
                "Lecture": {
                    "days":   [ "Tue", "Thu" ],
                    "time":   "13:00",
                    "length": 75
                }
            }
        }
    }
}'''))
print(s)

with open('test.ical', 'wb') as f:
  f.write(s.calendar().to_ical())
