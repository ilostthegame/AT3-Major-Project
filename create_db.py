#!/usr/bin/env python3
"""
Create database tables for the Flask app
"""
from flask_app import app, db

def create_database():
    """Create all database tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_database()