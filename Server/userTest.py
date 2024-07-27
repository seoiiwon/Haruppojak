from config.database import SessionLocal, engine
from models.UserModel import Base, UserInfo
from sqlalchemy.orm import sessionmaker
from models.DiaryModel import UserDiary

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create a new session
db = SessionLocal()