from flask_login import current_user, login_user, logout_user, login_required
from flask_app import app, db
from flask_app.models import User, Event
import sqlalchemy as sa
from flask import redirect, url_for, render_template, flash, request, session
from flask_app.forms import LoginForm, SignupForm, ChatbotForm, EventForm, AICalendarEventForm, GeneralSettingsForm, PasswordChangeForm, ClearCalendarForm
import os
from flask_app.chatbot import get_bot_reply, get_ai_event_string
import datetime

@app.route('/') 
def index():
    """Index route"""
    return redirect(url_for('login'))

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
    ai_form = AICalendarEventForm()
    # Manual event creation
    if form.submit.data and form.validate_on_submit():
        event = Event(
            title=form.title.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('calendar'))
    # Automated event creation using AI
    elif ai_form.submit_ai.data and ai_form.validate_on_submit():
        # Call your LLM here
        ai_event_str = get_ai_event_string(ai_form.prompt.data)
        if ai_event_str.strip() == 'Could not generate event string.':
            flash('Could not generate event string.')
            return redirect(url_for('calendar'))
        try:
            title, start, end = [s.strip().strip('`') for s in ai_event_str.split('|')]
            event = Event(
                title=title,
                start_time=datetime.datetime.fromisoformat(start),
                end_time=datetime.datetime.fromisoformat(end),
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
        except Exception as e:
            flash('Could not generate event string.')
        return redirect(url_for('calendar'))
    # Render the calendar page with existing events
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
    return render_template('calendar.html', events=events, form=form, ai_form=ai_form)

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
    general_form = GeneralSettingsForm(obj=current_user)
    password_form = PasswordChangeForm()
    clear_form = ClearCalendarForm()
    message = None

    if general_form.submit_general.data and general_form.validate_on_submit():
        current_user.confirm_delete_events = general_form.confirm_delete_events.data
        db.session.commit()
        message = 'Settings updated.'

    elif password_form.submit_password.data and password_form.validate_on_submit():
        current_user.set_password(password_form.new_password.data)
        db.session.commit()
        message = 'Password changed successfully.'

    elif clear_form.submit_clear.data and clear_form.validate_on_submit():
        Event.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        message = 'All events deleted.'

    return render_template('settings.html',
                           general_form=general_form,
                           password_form=password_form,
                           clear_form=clear_form,
                           message=message)
