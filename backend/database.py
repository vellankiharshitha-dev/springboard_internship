# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# SQLite file inside data/ folder
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()