import bcrypt

def hash_password(password: str) -> bytes:
    """Return bcrypt hashed password as BYTES."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    """Check bcrypt password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
