#!/bin/sh

CURL=$(which curl)
CURL_POST="$CURL -X POST"

HOST='http://localhost:5000'
#HOST='http://deschedule.hackafe.net'

SEMESTER="$HOST/api/umbc/semester"
BREAK="$HOST/api/umbc/semester/spring2016/break"
CLASS="$HOST/api/umbc/semester/spring2016/class"

$CURL_POST $SEMESTER/spring2016 \
    -d start=2016-01-27 \
    -d end=2016-05-10

$CURL_POST $BREAK \
    -d name="Spring Break" \
    -d start=2016-03-13 \
    -d end=2016-03-20

$CURL_POST $CLASS/CMSC491/2 \
    -d kind=Lecture \
    -d instructor="Hamed Pirsiavash" \
    -d days=tue/thu \
    -d time=13:00 \
    -d room=ITE233

$CURL_POST $CLASS/GERM102/1 \
    -d kind=Lecture \
    -d instructor="Susanne Sutton" \
    -d days=tue/thu \
    -d time=11:30 \
    -d room=ITE456

$CURL_POST $CLASS/GERM102/4 \
    -d kind=Discussion \
    -d days=mon \
    -d time=13:00 \
    -d length=50 \
    -d room=ITE237

$CURL_POST $CLASS/GES286/100 \
    -d kind=Lecture \
    -d instructor="Joseph School" \
    -d days=mon \
    -d time=08:30 \
    -d length=80 \
    -d room=MP101

$CURL_POST $CLASS/GES286/200 \
    -d kind=Laboratory \
    -d instructor="Joseph School" \
    -d days=wed \
    -d time=08:30 \
    -d length=140 \
    -d room=SOND007

$CURL_POST $CLASS/MATH407/1 \
    -d kind=Lecture \
    -d instructor="Thomas Armstrong" \
    -d days=tue/thu \
    -d time=16:00 \
    -d room=SOND112

$CURL_POST $CLASS/MATH430/1 \
    -d kind=Lecture \
    -d instructor="Weining Kang" \
    -d days=mon/wed \
    -d time=17:30 \
    -d room=SOND109
