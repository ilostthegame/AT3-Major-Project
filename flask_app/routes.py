from flask_login import current_user, login_user, logout_user, login_required
from flask_app import app, db
from flask_app.models import User
import sqlalchemy as sa
from flask import redirect, url_for, render_template, flash, request
from flask_app.forms import LoginForm, SignupForm
import google.generativeai as genai
import os

user = {'username': 'Bob Dylan'}

@app.route('/') 
def index():
    """Index route"""
    return redirect(url_for('login'))
    # TODO: Insert conditional for redirect based on user's authentication status.

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    # If the user is already authenticated, redirect to the calendar page
    if current_user.is_authenticated:
        return redirect(url_for('calendar'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        # If user is not found or password does not match, flash an error
        # message and redirect to login page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # If user is found and password matches, log the user in and redirect to the calendar page
        login_user(user)
        return redirect(url_for('calendar'))
    # If the form is not submitted or is invalid, render the login page
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Handles user logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup"""
    # If the user is already authenticated, redirect to the calendar page
    if current_user.is_authenticated:
        return redirect(url_for('calendar'))

    form = SignupForm()
    if form.validate_on_submit():
        # Add user to database after validating the form
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Automatically log in the user after successful signup
        login_user(user)
        return redirect(url_for('calendar'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/calendar')
@login_required
def calendar():
    """Calendar page"""
    return render_template('calendar.html', title='Calendar', user=user)

@app.route('/chatbot')
@login_required
def chatbot():
    """Chatbot page"""
    return render_template('chatbot.html')

@app.route('/chatbot_ask', methods=['POST'])
@login_required
def chatbot_ask():
    """Handles chatbot requests"""
    user_message = request.json.get('message', '')
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    print(app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    for m in genai.list_models():
        print(m.name, m.supported_generation_methods)
    try:
        response = model.generate_content(f"Please provide a helpful message about how to use this calendar app for this question: [question start] {user_message}. [question end] If this question is not related to the calendar app, please respond with 'I don't know'. Do not add markdown formatting to your response.")
        bot_reply = response.text.strip()
    except Exception as e:
        print(e)
        bot_reply = "Sorry, I couldn't process your request."
    return {"reply": bot_reply}
