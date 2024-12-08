import secrets
import string


def generate_api_key(length: int = 32) -> str:
    """Returns a cryptographically secure API key"""
    # Define the characters that can be used in the API key (uppercase, lowercase, digits, and special characters)
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a secure random API key
    api_key = "".join(secrets.choice(characters) for _ in range(length))
    return api_key
