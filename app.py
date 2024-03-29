from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

#creates tables in db if non exist.
db.create_all()


##################################################


@app.route('/')
def landing():
    """Redirect to users list"""
    posts = db.session.query(Post, User).join(User).all()
    posts.reverse()
    #
    return render_template("landing.html", posts=posts)


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
    #get all post of current user
    posts = Post.query.filter_by(user_id=userid).all()
    if user.image_url == "" or user.image_url is None:
        user.image_url = "https://eliaslealblog.files.wordpress.com/2014/03/user-200.png?w=700"
    return render_template("user-detail.html", user=user, posts=posts)


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


@app.route('/users/<int:userid>/posts', methods=["POST"])
def process_new_post_request(userid):
    """ Process new post into db"""
    # get data from post form
    post_title = request.form.get("post-title")
    post_content = request.form.get("post-content")
    # create db object
    new_post = Post(user_id=userid,
                    title=post_title, content=post_content)
    # add to db and commit
    db.session.add(new_post)
    db.session.commit()
    #
    return redirect(f"/users/{userid}")


@app.route('/posts/<int:postid>')
def show_post(postid):
    """Navigate to a user posts page"""
    post = Post.query.get_or_404(postid)
    user = User.query.get_or_404(post.user_id)
    return render_template("post-detail.html", post=post, user=user)


@app.route('/posts/<int:postid>/edit')
def edit_post_form(postid):
    """Show edit post form"""
    #
    post = Post.query.get_or_404(postid)
    user = User.query.get_or_404(post.user_id)

    return render_template("edit-post.html", post=post, user=user)


@app.route('/posts/<int:postid>/edit', methods=["POST"])
def process_edit_post_request(postid):
    """Process edit user form"""
    # get data from post form
    new_title = request.form.get("post-title")
    new_content = request.form.get("post-content")
    #
    post = Post.query.get_or_404(postid)
    post.title = new_title
    post.content = new_content
    #
    db.session.commit()
    #
    return redirect(f"/posts/{postid}")


@app.route('/posts/<int:postid>/delete', methods=["POST"])
def process_delete_post_request(postid):
    """Remove specified post from db"""
    #
    post = Post.query.get_or_404(postid)
    userid = post.user_id
    db.session.delete(post)
    db.session.commit()
    #
    return redirect(f"/users/{userid}")


##################################################


@app.route('/tags')
def tags_page():
    """Show list of Tags"""

    # get Tags from database
    list_of_tags = Tag.query.all()
    return render_template("tag-list.html", tags=list_of_tags)

@app.route('/tags/<int:tagid>')
def tag_details(tagid):
    """Navigate to a tags's page"""
    #get tag from db
    tag = Tag.query.get_or_404(tagid)

    posts_related_to_tag = tag.posts

    return render_template("show-tag.html", tag=tag, posts=posts_related_to_tag)
