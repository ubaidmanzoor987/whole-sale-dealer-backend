from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Session
import datetime
class Brands(Session.session.get_base()):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(50))
    own_brand = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id"))
    user_rel = relationship("User")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self,
                 brand_name=None,
                 user_id=None,
                 own_brand = None,
                 updated_at = None,
                 ):
        self.brand_name=brand_name
        self.own_brand = own_brand
        self.user_id=user_id
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def toDict(self):
        u = {"brand_id":self.id,"brand_name":self.brand_name, "own_brand":self.own_brand, "created_at": self.created_at,
            "updated_at": self.updated_at,}
        return u
