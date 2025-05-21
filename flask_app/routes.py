from flask_app import app
from flask import redirect, url_for, render_template, flash
from flask_app.forms import LoginForm, SignupForm

user = {'username': 'Bob Dylan'}

@app.route('/') 
def index():
    """Index route"""
    return redirect(url_for('login'))
    # TODO: Insert conditional for redirect based on user's authentication status.

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return render_template('login.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup"""
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup requested for user {}'.format(form.username.data))
        return render_template('signup.html', title='Sign Up', form=form)
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/calendar')
def calendar():
    """Calendar page"""

