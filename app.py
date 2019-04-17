"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config['SECRET_KEY'] = "SECRETTT"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "ADEFADEAA"

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def landing():
    """ """
    return render_template("edit-user.html")