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

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
