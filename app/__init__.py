from flask import Flask, render_template
from config import Config
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

# Load configuration
app.config.from_object(Config)

# Set up secret key for CSRF protection
app.config['SECRET_KEY'] = 'PASSWORD'

# Initialize extensions
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)

# Create the migration object
migrate = Migrate(app, root_db)

# Set the JSON encoder
app.json_encoder = JSONEncoder
