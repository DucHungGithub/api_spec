from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database connection settings
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "db"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Dependency to get a database session
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session