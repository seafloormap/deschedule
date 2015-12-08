#!/usr/bin/env python3

import sys
import argparse
import json

import cal

def main(args):
    with open(args.schedule, 'r') as f:
        s = cal.Semester.from_json_dict(json.load(f))
        c = s.calendar().to_ical()
        if args.output:
            with open(args.output, 'wb') as out:
                out.write(c)
        else:
            print(c.decode('utf-8'), end = '')

def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('schedule', type=str)
    parser.add_argument('output', type=str, nargs='?')

    return parser.parse_args(args)

if __name__ == '__main__':
    sys.exit(main(parse(sys.argv[1:])))
