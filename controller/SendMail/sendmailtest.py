"""
Unit tests for email validation module and Flask endpoints
"""

import pytest
import json
from controller.SendMail.sendmail import validate_email


# ============================================
# UNIT TESTS - Testing validation function directly
# ============================================

def test_valid_email_basic():
    """Test valid basic email"""
    result = validate_email("test@example.com")
    assert result['valid'] is True
    assert result['message'] == "Email is valid"
    assert result['email'] == "test@example.com"
    assert result['normalized'] == "test@example.com"


def test_valid_email_with_plus():
    """Test valid email with plus sign (Gmail style)"""
    result = validate_email("test+filter@example.com")
    assert result['valid'] is True
    assert result['normalized'] == "test+filter@example.com"


def test_valid_email_with_dots():
    """Test valid email with dots in local part"""
    result = validate_email("first.last@example.com")
    assert result['valid'] is True
    assert result['normalized'] == "first.last@example.com"


def test_valid_email_with_underscore():
    """Test valid email with underscore"""
    result = validate_email("first_last@example.com")
    assert result['valid'] is True


def test_valid_email_with_hyphen():
    """Test valid email with hyphen"""
    result = validate_email("first-last@example.com")
    assert result['valid'] is True


def test_valid_email_subdomain():
    """Test valid email with subdomain"""
    result = validate_email("user@mail.example.com")
    assert result['valid'] is True


def test_valid_email_multilevel_domain():
    """Test valid email with multi-level domain"""
    result = validate_email("user@example.co.uk")
    assert result['valid'] is True


# ============================================
# INVALID EMAIL TESTS
# ============================================

def test_empty_email():
    """Test empty email"""
    result = validate_email("")
    assert result['valid'] is False
    assert "required" in result['message'].lower()


def test_none_email():
    """Test None as email"""
    result = validate_email(None)
    assert result['valid'] is False


def test_too_short_email():
    """Test too short email"""
    result = validate_email("a@b.c")
    assert result['valid'] is False


def test_no_at_symbol():
    """Test email without @ symbol"""
    result = validate_email("testexample.com")
    assert result['valid'] is False
    assert "@" in result['message']


def test_no_local_part():
    """Test email with no local part"""
    result = validate_email("@example.com")
    assert result['valid'] is False
    assert "local part" in result['message'].lower()


def test_no_domain_part():
    """Test email with no domain part"""
    result = validate_email("test@")
    assert result['valid'] is False
    assert "domain part" in result['message'].lower()


def test_no_dot_in_domain():
    """Test email with no dot in domain"""
    result = validate_email("test@example")
    assert result['valid'] is False
    assert "dot" in result['message'].lower()


def test_consecutive_dots():
    """Test email with consecutive dots in local part"""
    result = validate_email("test..name@example.com")
    assert result['valid'] is False
    assert "consecutive dots" in result['message'].lower()


def test_invalid_characters_local():
    """Test email with invalid characters in local part"""
    result = validate_email("test!@example.com")
    assert result['valid'] is False
    assert "invalid characters" in result['message'].lower()


def test_invalid_characters_domain():
    """Test email with invalid characters in domain"""
    result = validate_email("test@exam!ple.com")
    assert result['valid'] is False
    assert "invalid characters" in result['message'].lower()


def test_domain_starts_with_hyphen():
    """Test email with domain starting with hyphen"""
    result = validate_email("test@-example.com")
    assert result['valid'] is False
    assert "hyphen" in result['message'].lower()


def test_local_part_too_long():
    """Test email with local part too long"""
    # Create a local part that's 65 characters long
    local_part = "a" * 65
    result = validate_email(f"{local_part}@example.com")
    assert result['valid'] is False
    assert "64" in result['message'] or "long" in result['message']


# ============================================
# PARAMETERIZED TESTS
# ============================================

@pytest.mark.parametrize("email,should_be_valid", [
    # Valid emails
    ("user@example.com", True),
    ("user.name@example.com", True),
    ("user-name@example.com", True),
    ("user_name@example.com", True),
    ("user+filter@example.com", True),
    ("user@mail.example.com", True),
    ("user@example.co.uk", True),
    ("123@example.com", True),
    ("user@sub.domain.com", True),
    
    # Invalid emails
    ("", False),
    ("user@", False),
    ("@example.com", False),
    ("user@example", False),
    ("user@.com", False),
    ("user..name@example.com", False),
    ("user!@example.com", False),
    ("user@exam!ple.com", False),
    ("a@b.c", False),
    ("user@-example.com", False),
])
def test_email_validation_parametrized(email, should_be_valid):
    """Test multiple emails at once"""
    result = validate_email(email)
    assert result['valid'] == should_be_valid


# ============================================
# FLASK ENDPOINT TESTS
# ============================================

def test_validate_endpoint_success(test_client):
    """Test POST /validate with valid email"""
    response = test_client.post(
        '/validate',
        json={'email': 'test@example.com'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is True
    assert data['email'] == 'test@example.com'
    assert data['normalized'] == 'test@example.com'


def test_validate_endpoint_invalid(test_client):
    """Test POST /validate with invalid email"""
    response = test_client.post(
        '/validate',
        json={'email': 'invalid-email'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['valid'] is False
    assert data['email'] == 'invalid-email'


def test_validate_endpoint_missing_email(test_client):
    """Test POST /validate with missing email field"""
    response = test_client.post(
        '/validate',
        json={}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing field' in data['message']


def test_validate_endpoint_empty_json(test_client):
    """Test POST /validate with empty JSON"""
    response = test_client.post(
        '/validate',
        json=None
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'JSON' in data['message']


def test_validate_endpoint_get(test_client):
    """Test GET /validate/<email> with valid email"""
    response = test_client.get('/validate/test@example.com')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is True
    assert data['email'] == 'test@example.com'


def test_validate_endpoint_get_invalid(test_client):
    """Test GET /validate/<email> with invalid email"""
    response = test_client.get('/validate/invalid-email')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['valid'] is False


def test_home_endpoint(test_client):
    """Test home endpoint returns API info"""
    response = test_client.get('/')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'service' in data
    assert 'endpoints' in data


# ============================================
# FIXTURE - Flask test client
# ============================================

@pytest.fixture
def test_client():
    """Create a Flask test client"""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client