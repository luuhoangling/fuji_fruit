"""Flask application factory"""

from flask import Flask
from app.extensions import init_extensions
from config import get_config
import os


def create_app(config_name=None):
    """Create and configure Flask application"""
    
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
    
    # Initialize custom database
    from app.db import init_db
    init_db(app)
    
    # Register Jinja filters
    @app.template_filter('vnd')
    def format_vnd(amount):
        """Format number as Vietnamese Dong currency"""
        if amount is None:
            return "0₫"
        return f"{int(amount):,}₫".replace(',', '.')
    
    # Import and register blueprints
    from app.api import api_bp, admin_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    
    # Import and register frontend blueprints
    from app.blueprints.site.views import site_bp
    from app.blueprints.admin.views import admin_bp as admin_frontend_bp
    app.register_blueprint(site_bp)
    app.register_blueprint(admin_frontend_bp, url_prefix='/admin')
    
    # Register error handlers
    from app.api.errors import register_error_handlers
    register_error_handlers(app)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('500.html'), 500
    
    return app