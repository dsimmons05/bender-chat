# manage.py
from gevent import monkey

monkey.patch_all()

import os
import unittest
import coverage

from flask import session
from flask.ext.socketio import SocketIO, emit, join_room

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from project import app, db
from project.models import User

import requests


app.config.from_object('project.config.DevelopmentConfig')

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)
socketio = SocketIO(app)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='project/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User("ad@min.com", "admin"))
    db.session.commit()

@socketio.on('message', namespace='/chat')
def chat_message(message):

    print message['data']

    emit('message', {'data': message['data']}, broadcast=True)

    data = message['data']
    ip = 'http://104.236.244.227:8080'
    msgs = requests.get(ip + '/data/chat').json()
    messages = msgs['data']
    messages += '[' + data['message'] + '] ' + data['author'] + '<br></br>'
    r = requests.post(ip + '/data', json = {'key':'chat', 'data':messages})
    print r.text

@socketio.on('connect', namespace='/chat')
def test_connect():
    ip = 'http://104.236.244.227:8080'

    msgs = requests.get(ip + '/data/chat').json()

    emit('load_msgs', {'msg': msgs}, broadcast=False)

@manager.command
def run():
    socketio.run(app, host='0.0.0.0')

if __name__ == '__main__':
    manager.run()
