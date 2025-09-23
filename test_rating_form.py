#!/usr/bin/env python3
"""
Test script để kiểm tra rating system
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.blueprints.site.forms import ReviewForm

def test_rating_form():
    """Test rating form validation"""
    app = create_app('testing')
    
    with app.app_context():
        print("Testing Rating Form")
        print("=" * 30)
        
        # Test different rating values
        test_cases = [
            {'rating': 1, 'content': 'Test content 1', 'expected': True},
            {'rating': 5, 'content': 'Test content 5', 'expected': True},
            {'rating': 3, 'content': 'Test content 3', 'expected': True},
            {'rating': 0, 'content': 'Test content 0', 'expected': False},  # Invalid
            {'rating': 6, 'content': 'Test content 6', 'expected': False},  # Invalid
            {'rating': 4, 'content': 'Test', 'expected': False},  # Too short content
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest case {i}: Rating={test_case['rating']}, Content='{test_case['content']}'")
            
            # Create form with test request context
            with app.test_request_context(method='POST', data=test_case):
                form = ReviewForm()
                form.rating.data = test_case['rating']
                form.content.data = test_case['content']
                form.user_name.data = 'Test User'
                
                is_valid = form.validate()
                print(f"Expected: {test_case['expected']}, Got: {is_valid}")
                
                if is_valid != test_case['expected']:
                    print(f"❌ FAILED - Form errors: {form.errors}")
                else:
                    print(f"✅ PASSED")
                    if is_valid:
                        print(f"   Rating value: {form.rating.data}")

if __name__ == "__main__":
    test_rating_form()