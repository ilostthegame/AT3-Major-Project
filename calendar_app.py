"""Imports the application instance"""
from flask_app import app

# Shell context - adding database instance to shell session
# For use in shell debugging.
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_app import app, db
from flask_app.models import User, Event

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Event': Event}