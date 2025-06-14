from flask_login import current_user, login_user, logout_user, login_required
from flask_app import app, db
from flask_app.models import User, Event
import sqlalchemy as sa
from flask import redirect, url_for, render_template, flash, request, session
from flask_app.forms import LoginForm, SignupForm, ChatbotForm, EventForm
import os
from flask_app.chatbot import get_bot_reply

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

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    """Handles calendar view and event creation"""
    form = EventForm()
    # Check if user is creating a new event
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('calendar'))
    
    # Else, render the calendar page with existing events
    events = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat(),
        }
        for event in db.session.scalars(
            sa.select(Event).where(Event.user_id == current_user.id)
        )
    ]
    return render_template('calendar.html', events=events, form=form)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Handles deletion of an event"""
    event = db.session.get(Event, event_id)
    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        return '', 204
    return '', 403

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    """Handles chatbot interaction"""
    form = ChatbotForm()
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    chat_history = session['chat_history']

    if form.validate_on_submit():
        user_msg = form.message.data
        form.message.data = ''  # Clear the input field after submission
        bot_reply = get_bot_reply(user_msg) 
        chat_history.append({'user': user_msg, 'bot': bot_reply})
        session['chat_history'] = chat_history
    return render_template('chatbot.html', form=form, chat_history=chat_history)

@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    """Handles predictive analysis of user data"""

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Handles user settings"""
