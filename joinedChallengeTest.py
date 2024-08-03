from Server.schemas.ChallengeSchema import UserChallenge
from Server.config.database import SessionLocal
from Server.models.UserModel import UserChallenge


Session = SessionLocal()

print(Session.query(UserChallenge).filter(UserChallenge.user_id == 2).all())

