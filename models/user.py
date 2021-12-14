import datetime
import json
import uuid
from functools import wraps

import jwt
from flask import request, jsonify
from sqlalchemy.dialects import postgresql
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, flask_app, AlchemyEncoder


class User(db.Model):
    id = db.Column(postgresql.UUID, primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(16), index=True, nullable=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password, name, email, phone):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.phone = phone

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def as_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'phone': self.phone,
            'name': self.name,
            'username': self.username,
        }

    def generate_token(self):
        return jwt.encode(self.as_dict(), flask_app.config['SECRET_KEY'], algorithm="HS256")

    def __repr__(self):
        return '<User %r>' % self.name
