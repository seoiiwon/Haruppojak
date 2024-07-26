from Server.config.database import SessionLocal, engine
from Server.models.UserModel import Base, UserInfo
from Server.models.DiaryModel import UserDiary
from sqlalchemy.orm import sessionmaker

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create a new session
db = SessionLocal()
