from gevent import monkey

monkey.patch_all()

import os
from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Creating database
engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()

# User Model 
class User(Base):

    __tablename__ = 'users'

    id          = Column(Integer, primary_key=True)
    username    = Column(String(64), unique=True)
    password    = Column(String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # These functions are needed to use with login 
    def is_authenticated(self):
        return True 

    def is_active(self):
        return True 

    def is_anonymous(self):
        return False 

    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)


Base.metadata.create_all(engine)

@login_manager.user_loader
def user_loader(user_id):
    # id's in Flask-login are Unicode strings --> let's convert 
    return db.session.query(User).get(int(user_id))

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@socketio.on('message', namespace='/chat')
def chat_message(message):
    print message['data']
    emit('message', {'data': message['data']}, broadcast = True)

@socketio.on('connect', namespace='/chat')
def test_connect():
    print "got a connection!"
    emit('my response', {'data': 'Connected', 'count': 0})

# @app.route('/lougout')
# def logout():
#     flask_login.logout_user()
#     return 'Logged out'

# init_login()


if __name__ == '__main__':
    socketio.run(app)
