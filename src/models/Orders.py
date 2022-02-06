from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from src.database.db import Session
import datetime
class Orders(Session.session.get_base()):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    quantites = Column(Integer)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))
    user_rel = relationship("User")
    product_id = Column(Integer, ForeignKey("products.id"))
    product_rel = relationship("Products")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self,
                 status=None,
                 quantites=None,
                 total_price=None,
                 user_id=None,
                 product_id = None,
                 updated_at = None,
                 ):
        self.status=status
        self.quantites=quantites
        self.total_price=total_price
        self.user_id=user_id
        self.product_id=product_id
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def toDict(self):
        u = {
            "order_id": self.id,
            "status": self.status,
            "quantites": self.quantites,
            "total_price": self.total_price,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if (self.product_rel):
            u["product_name"] = self.product_rel.product_name
            u["image1"] =  self.product_rel.image1
            u["image2"] =  self.product_rel.image2
            u["image3"] =  self.product_rel.image3
            if self.product_rel.brand_rel:
                u["brand_name"] =  self.product_rel.brand_rel.brand_name
            if self.product_rel.shopkeeper_rel:
                u["shopkeeper_owner_name"] = self.product_rel.shopkeeper_rel.owner_name
                u["shopkeeper_shop_name"] = self.product_rel.shopkeeper_rel.shop_name
                u["shopkeeper_address"] = self.product_rel.shopkeeper_rel.address
        if self.user_rel:
            u["customer_name"] = self.user_rel.owner_name
            u["customer_shop_name"] = self.user_rel.shop_name
            u["customer_shop_address"] = self.user_rel.address
        return u
