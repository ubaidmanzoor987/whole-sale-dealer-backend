from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from src.database.db import Session
import datetime
class ExpoPushTokens(Session.session.get_base()):
    __tablename__ = 'expo_push_tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    expo_push_token = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self,
                 user_id=None,
                 expo_push_token = None,
                 updated_at = None,
                 ):
        self.user_id=user_id
        self.expo_push_token=expo_push_token
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def toDict(self):
        u = {
            "expo_id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return u
