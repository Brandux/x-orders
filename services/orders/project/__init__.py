# services/users/project/__init__.py

import os  # nuevo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # nuevo
from flask_debugtoolbar import DebugToolbarExtension  # new
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# instanciando la db
db = SQLAlchemy()  # nuevo
toolbar = DebugToolbarExtension()  # new
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()


# new
def create_app(script_info=None):
    # instanciado la app
    app = Flask(__name__)

    # habilitando CORS
    # CORS(app)  # new


# establecer configuraicon
    app_settings = os.getenv('APP_SETTINGS')   # Nuevo
    app.config.from_object(app_settings)       # Nuevo


# set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)


# register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)


# shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
