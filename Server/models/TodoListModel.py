from sqlalchemy import *
from sqlalchemy.orm import relationship
# from config.database import Base
from Server.config.database import Base
from datetime import datetime


class TodoList(Base):
    __tablename__ = "todolist"
# userid
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    todo = Column(String, nullable=False)
    check = Column(Boolean, nullable=False, default=False)

    # 추천 todo리스트
    user_id = Column(Integer, nuallable=False)
    age_group = Column(String, nullable=False)
