from flask import Blueprint

bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from app.blueprints.api import routes
from app.blueprints.api import auth_routes
from app.blueprints.api import catalog_routes
from app.blueprints.api import cart_routes
from app.blueprints.api import order_routes
from app.blueprints.api import admin_routes