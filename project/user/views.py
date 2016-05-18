# project/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User
# from project.email import send_email
from project import db, bcrypt
from .forms import LoginForm, SignupForm


################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You registered and are now logged in. Welcome!', 'success')

        return render_template('user/chat_login.html')

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return render_template('user/chat_login.html')
        else:
            flash('Invalid username and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)

@user_blueprint.route('/chat_login')
def chat_login():
    return render_template('user/chat_login.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


