import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_app import db
from typing import Optional
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_app import login

@login.user_loader
def load_user(id):
    """Load a user by their ID."""
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    """User model"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    events: so.WriteOnlyMapped['Event'] = so.relationship(back_populates='user')

    def set_password(self, password):
        """Set the user's password after hashing it."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Event(db.Model):
    """Calendar event model"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    start_time: so.Mapped[datetime] = so.mapped_column()
    end_time: so.Mapped[datetime] = so.mapped_column()
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    user: so.Mapped[User] = so.relationship(back_populates='events')

    def __repr__(self):
        return '<Event {}>'.format(self.title)
