from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite na start
DATABASE_URL = "sqlite:///./wof.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # wymagane dla SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
