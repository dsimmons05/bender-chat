from flask import render_template, Blueprint
from flask.ext.login import login_required


################
#### config ####
################

chat_blueprint = Blueprint('chat', __name__,)


################
#### routes ####
################

@chat_blueprint.route('/chat')
@login_required
def chatroom():
    return render_template('chatroom.html')