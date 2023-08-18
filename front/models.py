from .database import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    lol_username = db.Column(db.String(150), default="None")
    matches = db.relationship('Match', backref='user', lazy=True)  # relationship with Match model

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_data = db.Column(db.Text)  # A placeholder, you can replace this with actual fields.
    analysis = db.Column(db.Text)  # Placeholder for analysis data.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
