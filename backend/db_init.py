from utils.database import init_db, SessionLocal, User
from backend.auth import hash_password

def main():
    print("Initializing database...")
    init_db()

    print("Creating a test user (if not exists)...")
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email="test@example.com").first()
        if user:
            print("Test user already exists.")
        else:
            hashed = hash_password("password123").decode('utf-8')
            u = User(full_name="Test User", email="test@example.com", hashed_password=hashed)
            db.add(u)
            db.commit()
            print("Test user created.")
    finally:
        db.close()
    print("Done.")

if __name__ == "__main__":
    main()
