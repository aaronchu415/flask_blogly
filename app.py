"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc

app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRETTT"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "ADEFADEAA"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route('/')
def landing():
    """Redirect to users list"""
    return redirect("/users")


@app.route('/users')
def render_users_page():
    """Show list of Users"""
    # get Users from database
    list_of_users = User.query.order_by(desc(User.id)).all()
    return render_template("landing.html", users=list_of_users)


@app.route('/users/new')
def render_new_user_page():
    """Show new user form"""
    return render_template("new-user.html")


@app.route('/users', methods=["POST"])
def process_new_user_request():
    """Process new user form"""
    # get data from user form
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")
    # create db object
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=img_url)
    # add to db and commit
    db.session.add(new_user)
    db.session.commit()
    #
    return redirect("/users")


@app.route('/users/<int:id>')
def render_user_details(id):
    """Navigate to a user's page"""
    user = User.query.get_or_404(id)
    return render_template("user-detail.html", user=user)


@app.route('/users/<int:id>/edit')
def edit_user_form(id):
    """Navigate to the edit user form"""
    user = User.query.get_or_404(id)
    return render_template("edit-user.html", user=user)


@app.route('/users/<int:id>/edit', methods=["POST"])
def process_edit_user_request(id):
    """Process edit user form"""
    # get data from user form
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")
    #
    user = User.query.get_or_404(id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url
    #
    db.session.commit()
    #
    return redirect(f"/users/{id}")


@app.route('/users/<int:id>/delete', methods=["POST"])
def process_delete_user_request(id):
    """Delete specified user"""
    #
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    #
    return redirect(f"/users")
