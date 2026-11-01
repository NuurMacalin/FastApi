
from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = "sqlite:///rangmanch.db"
engine = create_engine(DATABASE_URL)

def create_table():
    SQLModel.metadata.create_all(engine)
def connect_db():
    with Session(engine) as session:
        yield session

