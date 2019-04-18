"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text)

    def __repr__(self):
        return f'<{self.id},{self.first_name},{self.last_name}>'


class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id")) 
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow().strftime('%b %d %Y %H:%M:%S'))

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        return f'<{self.id},{self.title},{self.content}>'
