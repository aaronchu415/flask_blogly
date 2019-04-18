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
# db.create_all()


##################################################


@app.route('/')
def landing():
    """Redirect to users list"""
    return redirect("/users")


@app.route('/users')
def users_page():
    """Show list of Users"""
    # get Users from database
    list_of_users = User.query.order_by(desc(User.id)).all()
    return render_template("user-list.html", users=list_of_users)


@app.route('/users/new')
def new_user_form():
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


@app.route('/users/<int:userid>')
def user_details(userid):
    """Navigate to a user's page"""
    user = User.query.get_or_404(userid)
    if user.image_url == "" or user.image_url is None:
        user.image_url = "https://eliaslealblog.files.wordpress.com/2014/03/user-200.png?w=700"
    return render_template("user-detail.html", user=user)


@app.route('/users/<int:userid>/edit')
def edit_user_form(userid):
    """Navigate to the edit user form"""
    user = User.query.get_or_404(userid)
    return render_template("edit-user.html", user=user)


@app.route('/users/<int:userid>/edit', methods=["POST"])
def process_edit_user_request(userid):
    """Process edit user form"""
    # get data from user form
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")
    #
    user = User.query.get_or_404(userid)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url
    #
    db.session.commit()
    #
    return redirect(f"/users/{userid}")


@app.route('/users/<int:userid>/delete', methods=["POST"])
def process_delete_user_request(userid):
    """Delete specified user"""
    #
    user = User.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()
    #
    return redirect(f"/users")


##################################################

@app.route('/users/<int:userid>/posts/new')
def new_post_form(userid):
    """Show new post form"""
    #
    user = User.query.get_or_404(userid)
    return render_template("new-post.html", user=user)


# @app.route('/users/<int:userid>/posts', methods=["POST"])
# def process_new_post_request(userid):
#     """ """
#     #
#     return


# @app.route('/posts/<int:postid>')
# def show_post(postid):
#     """ """
#     #
#     return


# @app.route('/posts/<int:postid>/edit')
# def edit_post_form(postid):
#     """ """
#     #
#     return


# @app.route('/posts/<int:postid>/edit', methods=["POST"])
# def process_edit_post_request(postid):
#     """ """
#     #
#     return


# @app.route('/posts/<int:postid>/delete', methods=["POST"])
# def process_delete_post_request(postid):
#     """ """
#     #
#     return
