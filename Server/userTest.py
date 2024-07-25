from config.database import SessionLocal, engine
from models.UserModel import Base, UserInfo
from sqlalchemy.orm import sessionmaker

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create a new session
db = SessionLocal()

try:
    # Create a new user
    user = UserInfo(
        userID="test",
        userPassword="test_password",  # Add a user password field or set it to None
        userName="김멋사",
        userBirth=990829,
        userEmail="test@gmail.com",
        userGender=1,
        userPpojakCoin=0,
        userProfileName="test",
        userProfileComment="",
        role="ADMIN"  # Ensure the role is in uppercase
    )

    # Add the user to the session
    db.add(user)
    
    # Commit the session
    db.commit()
    
    # Refresh the user instance to get the ID
    db.refresh(user)

    print(f"User {user.userID} created with ID {user.id}")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")

finally:
    db.close()
