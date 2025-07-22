from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeLocalField, SelectField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo 
import sqlalchemy as sa
from flask_app import db
from flask_app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    """Form for user signup."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), 
                                                                   EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if the username already exists in the database."""
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username already exists.')
        
    def validate_email(self, email):
        """Check if the email already exists in the database."""
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email already exists.')
    
    def validate_password(self, password):
        """Ensure password meets security requirements."""
        pw = password.data
        if len(pw) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(c.islower() for c in pw):
            raise ValidationError('Password must contain a lowercase letter.')
        if not any(c.isupper() for c in pw):
            raise ValidationError('Password must contain an uppercase letter.')
        if not any(c.isdigit() for c in pw):
            raise ValidationError('Password must contain a digit.')
        if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in pw):
            raise ValidationError('Password must contain a special character.')

class EventForm(FlaskForm):
    """Form for creating a new calendar event."""
    title = StringField('Title', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Event')

    def validate_end_time(self, end_time):
        if end_time.data < self.start_time.data:
            raise ValidationError('End time must be after start time.')

class ChatbotForm(FlaskForm):
    """Form for chatbot interaction."""
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class GeneralSettingsForm(FlaskForm):
    """Form for general user settings."""
    confirm_delete_events = BooleanField('Require confirmation when deleting events')
    submit_general = SubmitField('Save Settings')

class PasswordChangeForm(FlaskForm):
    """Form for changing user password."""
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit_password = SubmitField('Change Password')

    def validate_old_password(self, field):
        """Ensure input is equal to user's current password"""
        if not current_user.check_password(field.data):
            raise ValidationError('Current password is incorrect')

    def validate_new_password(self, new_password):
        """Ensure password meets security requirements."""
        pw = new_password.data
        if len(pw) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(c.islower() for c in pw):
            raise ValidationError('Password must contain a lowercase letter.')
        if not any(c.isupper() for c in pw):
            raise ValidationError('Password must contain an uppercase letter.')
        if not any(c.isdigit() for c in pw):
            raise ValidationError('Password must contain a digit.')
        if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in pw):
            raise ValidationError('Password must contain a special character.')

class ClearCalendarForm(FlaskForm):
    """Form for clearing the calendar."""
    submit_clear = SubmitField('Clear All Events')

class AICalendarEventForm(FlaskForm):
    """Form for automated event addition"""
    prompt = StringField('Describe your event', validators=[DataRequired()])
    submit_ai = SubmitField('Add Event With AI')