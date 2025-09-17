"""
Authentication API routes
"""
from flask import jsonify, request
from app.blueprints.api import bp
from app.auth import register_user, authenticate_user, generate_access_token, get_current_user, login_required
import logging

logger = logging.getLogger(__name__)

def make_json_response(data, status=200):
    """Create a JSON response with proper UTF-8 encoding"""
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, status

@bp.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return make_json_response({
                    'error': f'{field} is required'
                }, 400)
        
        # Register user
        user, error = register_user(
            email=data['email'],
            password=data['password'],
            full_name=data['full_name'],
            phone=data['phone']
        )
        
        if error:
            return make_json_response({
                'error': error
            }, 400)
        
        # Generate access token
        access_token = generate_access_token(user.id)
        
        return make_json_response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'role_code': user.role_code
            },
            'access_token': access_token
        }, 201)
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return make_json_response({
            'error': 'Registration failed'
        }, 500)

@bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return make_json_response({
                'error': 'Email and password are required'
            }, 400)
        
        # Authenticate user
        user, error = authenticate_user(
            email=data['email'],
            password=data['password']
        )
        
        if error:
            return make_json_response({
                'error': error
            }, 400)
        
        # Generate access token
        access_token = generate_access_token(user.id)
        
        return make_json_response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'role_code': user.role_code
            },
            'access_token': access_token
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return make_json_response({
            'error': 'Login failed'
        }, 500)

@bp.route('/auth/me', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    try:
        user = get_current_user()
        return make_json_response({
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'role_code': user.role_code
            }
        })
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get profile'
        }, 500)

@bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint (client-side token removal)"""
    return make_json_response({
        'message': 'Logout successful'
    })