# app/__init__.py
import os
from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load the config
    app.config.from_object('app.config.Config')

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from . import database
    database.init_app(app)

    # <<<--- ADD THIS PART --- S>>>
    # Import and register the blueprint
    from . import routes
    app.register_blueprint(routes.api_bp, url_prefix='/api')
    # <<<--- END OF ADDED PART --- S>>>

    # A simple test route
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app