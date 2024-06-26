from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Ensure metadata is defined
metadata = MetaData()

# Define the engine and session
engine = create_engine('sqlite:///example.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example table definition
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Function to create tables
def create_user(username: str, password: str):
    session = SessionLocal()
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()

def get_user(username: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user

# Ensure the database is created
Base.metadata.create_all(bind=engine)
