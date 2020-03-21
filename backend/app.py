from flask import Flask, redirect, url_for, session, render_template, request, Response
from flask_login import LoginManager, login_user, current_user, login_required
from flask_session import Session
import logging

from model import User
from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

def response_invalid_request():
    """
    Response to an invalid request.
    :return: JSON
    """
    _response = {}
    _response['Status'] = 400
    _response['Success'] = False
    _response['Result'] = 'Invalid request.'
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=400,
                    mimetype="application/json")

def response_unauthorized_request():
    """
    Response to an unauthorized request.
    :return: JSON
    """
    _response = {}
    _response['Success'] = False
    _response['Status'] = 401
    _response['Result'] = 'Unauthorized request.'
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=401,
                    mimetype="application/json")

def response_valid_request(data):
    """
    Response to a valid request.
    :return: JSON wthat contains the input data
    """
    _response = {}
    _response['Success'] = True
    _response['Status'] = 200
    _response['Result'] = data
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=200,
                    mimetype="application/json")

#Main page, ToDo: create main page template
@app.route('/')
@login_required
def index():
    return "Welcome"

#compare the user id with the known sessions
@login_manager.user_loader
def load_user(id):
    if 'users' in session.keys():
        if int(id) in session['users'].keys():
            return session['users'][int(id)]
        else:
            return None
    else:
        session['users'] = {}
    return id

#Login page for the user
@app.route('/login')
def login_page():
    return render_template("login_form.html")

#Page where the data entered in the login page gets validated
#If validation not successful, it moves back to the login page
@app.route('/logged-in', methods=['POST'])
def loggedin_page():
    username = request.form["username"]
    password = request.form["password"]
    #ToDo: database check if we know this user and the password is correct
    if (password == '1234' and username == 'test'):
        session.clear()
        if not 'users' in session.keys():
            session['users'] = {}
        user = User({"id":0, "name":"Horst"})
        session['users'][user.id] = user
        login_user(user)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run()
