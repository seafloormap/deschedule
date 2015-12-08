#!/usr/bin/env python3

import cal
import datetime

s = cal.Semester(
    start   = datetime.date(2016, 1, 25),
    end     = datetime.date(2016, 5, 10),
    classes = {
      'ABCD 101': cal.Class({
        'Lecture': cal.Section(
          days   = [ 2, 4 ],
          time   = datetime.time(13, 0),
          length = datetime.timedelta(minutes=75))
        })
    })

print(s.calendar())
print(s.calendar().to_ical().decode('utf-8'))
