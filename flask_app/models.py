import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_app import db
from typing import Optional
from datetime import datetime, timezone

class User(db.Model):
    """User model"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    events: so.WriteOnlyMapped['Event'] = so.relationship(back_populates='user')

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