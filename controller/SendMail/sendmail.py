"""
Email validation module with Flask integration
"""

import re
from typing import Dict, Any


def validate_email(email: str) -> Dict[str, Any]:
    """
    Validates an email address and returns validation result.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        Dict containing:
            - valid (bool): True if email is valid
            - message (str): Validation message
            - email (str): The original email
            - normalized (str): Normalized email (if valid)
    """
    # Check if email is empty
    if not email:
        return {
            "valid": False,
            "message": "Email address is required",
            "email": email,
            "normalized": None
        }
    
    # Basic checks
    if not isinstance(email, str):
        return {
            "valid": False,
            "message": "Email must be a string",
            "email": str(email),
            "normalized": None
        }
    
    # Clean the email (remove whitespace)
    email = email.strip()
    
    # Validate length
    if len(email) < 5:
        return {
            "valid": False,
            "message": "Email is too short",
            "email": email,
            "normalized": None
        }
    
    if len(email) > 254:
        return {
            "valid": False,
            "message": "Email is too long (max 254 characters)",
            "email": email,
            "normalized": None
        }
    
    # Check for @ symbol
    if "@" not in email:
        return {
            "valid": False,
            "message": "Email must contain @ symbol",
            "email": email,
            "normalized": None
        }
    
    # Split into local and domain parts
    local_part, domain_part = email.rsplit("@", 1)
    
    # Check local part
    if not local_part:
        return {
            "valid": False,
            "message": "Email must have a local part before @",
            "email": email,
            "normalized": None
        }
    
    if len(local_part) > 64:
        return {
            "valid": False,
            "message": "Local part is too long (max 64 characters)",
            "email": email,
            "normalized": None
        }
    
    # Check domain part
    if not domain_part:
        return {
            "valid": False,
            "message": "Email must have a domain part after @",
            "email": email,
            "normalized": None
        }
    
    # Check for dot in domain
    if "." not in domain_part:
        return {
            "valid": False,
            "message": "Domain must contain a dot (.)",
            "email": email,
            "normalized": None
        }
    
    # Check domain length
    if len(domain_part) < 3:
        return {
            "valid": False,
            "message": "Domain is too short",
            "email": email,
            "normalized": None
        }
    
    # Check for valid characters in local part (basic check)
    # Allow: letters, numbers, dots, underscores, hyphens, plus
    valid_local_chars = re.match(r'^[a-zA-Z0-9._%+-]+$', local_part)
    if not valid_local_chars:
        return {
            "valid": False,
            "message": "Local part contains invalid characters",
            "email": email,
            "normalized": None
        }
    
    # Check for consecutive dots in local part
    if ".." in local_part:
        return {
            "valid": False,
            "message": "Local part cannot contain consecutive dots",
            "email": email,
            "normalized": None
        }
    
    # Check domain has valid characters
    valid_domain_chars = re.match(r'^[a-zA-Z0-9.-]+$', domain_part)
    if not valid_domain_chars:
        return {
            "valid": False,
            "message": "Domain contains invalid characters",
            "email": email,
            "normalized": None
        }
    
    # Check domain doesn't start or end with hyphen
    if domain_part.startswith("-") or domain_part.endswith("-"):
        return {
            "valid": False,
            "message": "Domain cannot start or end with a hyphen",
            "email": email,
            "normalized": None
        }
    
    # All validation passed!
    normalized = email.lower()
    
    return {
        "valid": True,
        "message": "Email is valid",
        "email": email,
        "normalized": normalized
    }