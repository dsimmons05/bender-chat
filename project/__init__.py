# project/__init__.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

#### config ####
app = Flask(__name__)

app.config.from_object('project.config.DevelopmentConfig')

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


def import_blueprints():
    from project.main.views import main_blueprint
    from project.user.views import user_blueprint
    from project.chat.views import chat_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(chat_blueprint)

import_blueprints()

from project.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
