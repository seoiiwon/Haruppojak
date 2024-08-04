from Server.config.database import SessionLocal
from Server.models.UserModel import UserChallenge
from Server.models.ChallengeModel import Challenge

db = SessionLocal()

# user_challenge = [db.query(UserChallenge).filter(UserChallenge.user_id == 1).first()]
user_challenge = db.query(UserChallenge).filter(UserChallenge.user_id == 1).first()

print(user_challenge.challenge_id)

# challenge = [db.query(ChallengeModel) for i in user_challenge]
# challenge = db.query(Challenge).filter(Challenge.id == )


challenge = db.query(Challenge).filter(user_challenge.id == )