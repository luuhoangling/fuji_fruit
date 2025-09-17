from flask import Flask
from config import get_config
from app.db import init_db
from app.models import models
import logging
import os

def create_app(config_name=None):
    """Application factory function"""
    
    # Determine config name
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Setup logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    try:
        with app.app_context():
            init_db(app)
            models.init_models()
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {str(e)}")
        # In development, we might want to continue without DB for testing
        if config_name == 'development':
            app.logger.warning("Continuing without database connection in development mode")
        else:
            raise
    
    # Register blueprints
    from app.blueprints.public import bp as public_bp
    from app.blueprints.api import bp as api_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add a simple root route that redirects to public blueprint
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('public.index'))
    
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