from flask import Flask, redirect, url_for, session, render_template, request
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
