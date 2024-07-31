from sqlalchemy.orm import Session
from Server.config.database import SessionLocal
from Server.models.ChallengeModel import Challenge

def delete_all_challenges(db: Session):
    challenge_all = db.query(Challenge).all()
    for challenge in challenge_all:
        db.delete(challenge)
    db.commit()
    db.close()

db = SessionLocal()
delete_all_challenges(db)
