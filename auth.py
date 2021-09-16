import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# Create Blueprint() named 'auth'
# __name__ provides location of file to bp
# url_prefix prepends URLs associated with bp
bp = Blueprint("auth", __name__, url_prefix="/auth")


# Associate URL /register with register view fn
@bp.route("/register", methods=("GET", "POST"))
def register():
    # Begin validation if True
    # True if user submits register form
    if request.method == "POST":
        username = request.form["username"]  # Dict mapping
        password = request.form["password"]  # Dict mapping
        db = get_db()
        error = None

        if not username:
            error = "Username is required."  # Empty?
        elif not password:
            error = "Password is required."  # Empty?
        elif (
            # Fetch one matching row of selection
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None  # Username taken?
        ):
            error = f"User {username} is already registered."

        if error is None:
            db.execute(  # Store into and update db
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("auth.login"))  # Generate URL, redirect

        flash(error)

    return render_template("auth/register.html")


# /login uses same pattern as /register
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(  # Query username
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."  # Validate password
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            # session is a dict that stores the user's login session across
            # requests by securely cookie'ing their data back to them.
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
# Register function to run before view
def load_logged_in_user():
    user_id = session.get("user_id")  # Check session for user

    if user_id is None:
        g.user = None
    else:
        g.user = (  # Store logged in user's data (for this request)
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# Require auth for posting, editing, etc.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # auth.login == blueprint.method
            return redirect(url_for("auth.login"))
        else:
            return view(**kwargs)

    return wrapped_view
