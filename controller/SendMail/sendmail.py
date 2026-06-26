"""
Email validation module
"""

import re
from typing import Dict, Any


def validate_email(email: str) -> Dict[str, Any]:
    """
    Validates an email address and returns validation result.
    """
    # Check if email is empty
    if not email:
        return {
            "valid": False,
            "message": "Email address is required",
            "email": email,
            "normalized": None
        }
    
    # Check if email is None or wrong type
    if not isinstance(email, str):
        return {
            "valid": False,
            "message": "Email must be a string",
            "email": str(email),
            "normalized": None
        }
    
    # Clean the email
    email = email.strip()
    
    # ✅ FIX: Change minimum length from 5 to 3 (so "a@b.c" passes)
    if len(email) < 3:  # Changed from 5 to 3
        return {
            "valid": False,
            "message": "Email is too short",
            "email": email,
            "normalized": None
        }
    
    if len(email) > 254:
        return {
            "valid": False,
            "message": "Email is too long",
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
            "message": "Local part is too long",
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
    
    # Check for valid characters in local part
    valid_local_chars = re.match(r'^[a-zA-Z0-9._%+-]+$', local_part)
    if not valid_local_chars:
        return {
            "valid": False,
            "message": "Local part contains invalid characters",
            "email": email,
            "normalized": None
        }
    
    # Check for consecutive dots
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
    return {
        "valid": True,
        "message": "Email is valid",
        "email": email,
        "normalized": email.lower()
    }