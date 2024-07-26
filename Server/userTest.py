from config.database import SessionLocal, engine
from models.UserModel import Base, UserInfo
from models.DiaryModel import Base, UserDiary
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create a new session
db = SessionLocal()

try:
    # Create a new user
    diary = UserDiary(
        Date=datetime.now(),
        Diarycontent="김뽀작의 일기장",
        Response="안녕 뽀짝아",
        Diarytodo=""  # Ensure the role is in uppercase
    )

    # Add the user to the session
    db.add(diary)
    
    # Commit the session
    db.commit()
    
    # Refresh the user instance to get the ID
    db.refresh(diary)

    print(f"User {diary.Diarycontent} created with ID {diary.id}")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")

finally:
    db.close()
