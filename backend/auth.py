# backend/auth.py
from sqlalchemy.orm import Session
from .models import User
from .database import SessionLocal
import hashlib

def hash_password(plain: str) -> str:
    return hashlib.sha256(plain.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed

def create_user(full_name: str, email: str, password: str):
    db: Session = SessionLocal()

    hashed = hash_password(password)

    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_user_by_email(email: str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user