"""Flask application factory"""

from flask import Flask
from app.extensions import init_extensions
from app.api import api_bp, admin_bp


def create_app(config_name=None):
    """Create and configure Flask application"""
    import os
    from config import get_config
    
    # Determine config
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    
    # Register error handlers
    from app.api.errors import register_error_handlers
    register_error_handlers(app)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app