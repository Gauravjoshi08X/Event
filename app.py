"""
Flask API for email validation
"""

from flask import Flask, request, jsonify
from controller.SendMail.sendmail import validate_email

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "service": "Email Validation API",
        "version": "1.0.0",
        "endpoints": {
            "/validate": "POST - Validate an email address",
            "/validate/<email>": "GET - Validate an email address"
        },
        "usage": {
            "POST": {
                "body": '{"email": "test@example.com"}',
                "content_type": "application/json"
            },
            "GET": {
                "url": "/validate/test@example.com"
            }
        }
    })


@app.route('/validate', methods=['POST'])
def validate_email_endpoint():
    """
    Validate an email address via POST request.
    
    Expected JSON body:
        {"email": "test@example.com"}
    
    Returns:
        JSON response with validation result
    """
    try:
        # Parse JSON request body
        data = request.get_json()
        
        # Check if JSON was provided
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON",
                "valid": False
            }), 400
        
        # Check if 'email' field exists
        if 'email' not in data:
            return jsonify({
                "error": "Missing field",
                "message": "Request must contain 'email' field",
                "valid": False
            }), 400
        
        # Get email from request
        email = data.get('email')
        
        # Validate the email
        result = validate_email(email)
        
        # Return appropriate status code
        if result['valid']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e),
            "valid": False
        }), 500


@app.route('/validate/<string:email>', methods=['GET'])
def validate_email_get(email):
    """
    Validate an email address via GET request.
    
    URL pattern:
        /validate/test@example.com
    
    Returns:
        JSON response with validation result
    """
    try:
        # Validate the email
        result = validate_email(email)
        
        # Return appropriate status code
        if result['valid']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e),
            "valid": False
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "This endpoint does not support this HTTP method"
    }), 405


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)