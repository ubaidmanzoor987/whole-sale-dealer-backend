from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.db import Session
class Brands(Session.session.get_base()):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(50))
    own_brand = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id"))
    user_rel = relationship("User")

    def __init__(self,
                 brand_name=None,
                 user_id=None,
                 own_brand = None
                 ):
        self.brand_name=brand_name
        self.own_brand = own_brand
        self.user_id=user_id

    def toDict(self):
        u = {"brand_id":self.id,"brand_name":self.brand_name, "own_brand":self.own_brand}
        return u
