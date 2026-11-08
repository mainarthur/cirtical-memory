"""Authentication module."""

def verify_token(token: str) -> bool:
    return token.startswith("valid_")

