import re
import bcrypt
from utils.database import create_user, get_user_by_email

# EMAIL VALIDATION

def validate_email(email: str) -> bool:
    """Validate basic email format."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

# PASSWORD VALIDATION 

def validate_password(password: str) -> tuple[bool, str]:
    """
    Password must follow rules:
    - Minimum 8 characters
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 number
    - At least 1 special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, ""

# USER REGISTRATION 

def register_user(full_name: str, email: str, password: str, confirm_password: str):
    """
    Handles user registration.
    Returns (success: bool, message: str)
    """

    full_name = full_name.strip()
    email = email.strip().lower()

    # Validate name
    if not full_name:
        return False, "Full name cannot be empty."

    # Validate email
    if not validate_email(email):
        return False, "Invalid email format."

    # Validate password match
    if password != confirm_password:
        return False, "Password and Confirm Password do not match."

    # Validate password strength
    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg

    # Check if email already exists
    existing = get_user_by_email(email)
    if existing is not None:
        return False, "User with this email already exists."

    # Hash the password
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        create_user(full_name, email, hashed_pw)
        return True, "Registration successful! You can now log in."
    except Exception as e:
        print("Error in register_user:", e)
        return False, "Something went wrong while creating the user."

# USER LOGIN LOGIC

def login_user(email: str, password: str):
    """
    Handles user login.
    Returns (success: bool, message: str, user: dict | None)
    """

    email = email.strip().lower()

    user = get_user_by_email(email)
    if user is None:
        return False, "Invalid email or password.", None

    stored_hash = user["password_hash"]

    # Compare entered password with stored hash
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, "Login successful!", user
    else:
        return False, "Invalid email or password.", None