# tools/delete_user.py
import os
import sys

# ensure project root is on sys.path so "from utils..." works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.database import SessionLocal, User

def main():
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email="test@example.com").first()
        if user:
            print("Found user:", user.email)
            db.delete(user)
            db.commit()
            print("User deleted successfully!")
        else:
            print("User not found.")
    finally:
        db.close()

if __name__ == "__main__":
    main()