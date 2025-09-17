from flask import Blueprint

bp = Blueprint('public', __name__, template_folder='templates')

# Import routes to register them with the blueprint
from app.blueprints.public import routes