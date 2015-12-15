#!flask/bin/python
import sys, os, argparse

basedir = os.path.abspath(os.path.dirname(__file__))

def main(args):
    from app import app
    app.config['SQLALCHEMY_DATABASE_URI'] = args.db
    app.config['SQLALCHEMY_MIGRATE_REPO'] = args.migrate
    app.config.from_object(args.config)

    if args.create:
        from app import db
        db.create_all()

    app.run(host=args.host, port=args.port, debug=args.debug)

def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('config', default='config', nargs='?')
    parser.add_argument('--db', default='sqlite:///' + os.path.join(basedir, 'app.db'))
    parser.add_argument('--migrate', default=os.path.join(basedir, 'db_repository'))
    parser.add_argument('--create', action='store_false', default=True)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--debug', action='store_true', default=False)
    return parser.parse_args(args)

if __name__ == '__main__':
    sys.exit(main(parse(sys.argv[1:])))

