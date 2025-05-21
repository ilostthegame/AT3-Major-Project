from flask_app import app
from flask import redirect, url_for, render_template
from flask_app.forms import LoginForm

user = {'username': 'Bob Dylan'}

@app.route('/') 
def index():
    """Index route"""
    return redirect(url_for('login'))
    # TODO: Insert conditional for redirect based on user's authentication status.

@app.route('/login')
def login():
    """Handles user login"""

    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup')
def signup():
    """Handles user signup"""

@app.route('/calendar')
def calendar():
    """Calendar page"""

