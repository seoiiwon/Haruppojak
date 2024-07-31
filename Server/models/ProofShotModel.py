from sqlalchemy import *
from sqlalchemy.orm import relationship
from Server.config.database import Base
from datetime import datetime

class ProofShot(Base):
    __tablename__ = "proofShot"

    id = Column(Integer, primary_key=True)
    userID = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    photoComment = Column(String, nullable=True, default="")

    participants = relationship('UserProofShot', back_populates='proofShot')