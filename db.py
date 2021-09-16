import sqlite3


import click
from flask import current_app, g

# current_app points to "this" Flask app.
# g is unique for each request. It stores data to be used during the request,
# and (e.g.) is reused if get_db() is called again during the same request.

from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(  # Connect to file found in database config
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db


# Check if g.db was set
# Check if a connection was created
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()  # Database connection
    # open_resource relative to the flaskr pkg
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# Define cl command
@click.command("init-db")
@with_appcontext
def init_db_command():
    # Clear existing data, create new tables
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    # close_db after each request
    app.teardown_appcontext(close_db)

    # Add new command callable with `flask`
    app.cli.add_command(init_db_command)


# Init db with:
"""flask init-db"""
# Look for flaskr.sqlite in instance/
