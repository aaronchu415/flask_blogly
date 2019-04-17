"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
user_1 = User(first_name='Test1', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
user_2 = User(first_name='Test2', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
user_3 = User(first_name='Test3', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
user_4 = User(first_name='Test4', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
user_5 = User(first_name='Test5', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')

# Add new objects to session, so they'll persist
db.session.add(user_1)
db.session.add(user_2)
db.session.add(user_3)
db.session.add(user_4)
db.session.add(user_5)

# Commit--otherwise, this never gets saved!
db.session.commit()