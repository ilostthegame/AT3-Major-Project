from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from flask_app import db
from flask_app.models import User

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
        if not any(c in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~" for c in pw):
            raise ValidationError('Password must contain a special character.')

class ChatbotForm(FlaskForm):
    """Form for chatbot interaction."""
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')