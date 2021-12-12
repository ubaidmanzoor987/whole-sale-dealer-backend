from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database.db import Session

class Products(Session.session.get_base()):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    image1 = Column(String)
    image2 = Column(String)
    image3 = Column(String)
    price = Column(Float)
    quantities = Column(Float)
    product_des = Column(String(150),nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    brand_rel = relationship("Brands")
    shopkeeper_rel = relationship("User")
    def __init__(self,
                 product_name=None,
                 image1=None,
                 image2=None,
                 image3=None,
                 price =None,
                 product_des= None,
                 brand_id = None,
                 user_id = None,
                 quantities = None,
                 ):
        self.product_name = product_name
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.price= price
        self.product_des = product_des
        self.brand_id = brand_id
        self.user_id = user_id
        self.quantities = quantities

    def toDict(self):
        u = {
                "product_id" : self.id,
                "product_name": self.product_name,
                "image1": str(self.image1),
                "image2": str(self.image2),
                "image3": str(self.image3),
                "price": self.price,
                "quantities": self.quantities,
                "product_des": self.product_des,
                "brand_id":self.brand_id,
                "user_id":self.user_id
        }
        if(self.brand_rel):
            u["brand_name"] = self.brand_rel.brand_name
        return u
