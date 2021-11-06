import os
from flask import Flask


def create_app(test_config=None):
    # Application factory function
    # Config files relative to instance/
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # Load instance config (if not testing & exists)
        # Will override default configuration using config.py
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Or load test config (if passed in)
        app.config.from_mapping(test_config)

    try:
        # Ensure instance/ exists
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    # Import and register blog.bp
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    # Unlike the auth blueprint, the blog blueprint does not have a url_prefix.
    # So the index view will be at /, the create view at /create, and so on.
    # The blog is the main feature of Flaskr, so it makes sense that the blog
    # index will be the main index.

    # However, the endpoint for the index view defined below will be
    # blog.index. Some of the authentication views referred to a plain index
    # endpoint. app.add_url_rule() associates the endpoint name 'index' with
    # the / url so that url_for('index') or url_for('blog.index') will both
    # work, generating the same / URL either way.

    # In another application you might give the blog blueprint a url_prefix and
    # define a separate index view in the application factory, similar to the
    # hello view. Then the index and blog.index endpoints and URLs would be
    # different.

    return app
