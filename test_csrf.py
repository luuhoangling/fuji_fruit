"""Test script để kiểm tra CSRF token hoạt động"""

from app import create_app
from flask_wtf.csrf import generate_csrf
from flask import render_template_string

app = create_app()

with app.test_request_context():
    # Test CSRF token generation
    try:
        token = generate_csrf()
        print(f"CSRF token generated successfully: {token[:20]}...")
        
        # Test template rendering with CSRF
        template = """
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
            <input type="text" name="test" value="test">
        </form>
        """
        
        rendered = render_template_string(template)
        print("Template rendering with CSRF successful")
        print("Form contains CSRF token:", 'csrf_token' in rendered)
        
    except Exception as e:
        print(f"Error: {e}")