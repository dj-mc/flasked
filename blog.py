from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort


from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint("blog", __name__)  # Define new bp in app factory


@bp.route("/")
def index():
    """
    /index displays most recent posts.
    """
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"  # JOIN author's info
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


# The create view is similar to the auth register view:
# - display a form
# - validate POST data --> add to database
# - or show an error


@bp.route("/create", methods=("GET", "POST"))
@login_required  # User must be logged in!
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


# Both update/delete views fetch posts via id and
# check if logged in user == author.


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        # Raise exception, return HTTP status code
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)  # Forbidden

    return post


# URL e.g. /1/update
# url_for('blog.update', id=post['id'])
# Get a post without checking its author
@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):  # The route's <int:id>
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


# Delete view has no template
# Delete button found in update.html
@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    # Handle POST then redirect to index
    return redirect(url_for("blog.index"))
