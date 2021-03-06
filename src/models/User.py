from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from src.database.db import Session
import datetime
class User(Session.session.get_base()):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(120), unique=True)
    owner_name = Column(String(50))
    shop_name = Column(String(250))
    owner_phone_no = Column(String(20))
    shop_phone_no1 = Column(String(20))
    shop_phone_no2 = Column(String(20))
    loc_long = Column(Float)
    loc_lat = Column(Float)
    address = Column(String(250))
    password = Column(String(120))
    image = Column(String(500))
    email = Column(String(120), unique=True)
    relevant_id = Column(JSON)
    token = Column(String(500))
    expo_push_token = Column(String(500))
    user_type = Column(String(200))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    def __init__(self,
                 user_name = None,
                 shop_name=None,
                 password=None,
                 owner_name=None,
                 owner_phone_no=None,
                 shop_phone_no1=None,
                 shop_phone_no2=None,
                 loc_long=None,
                 loc_lat=None,
                 address=None,
                 image=None,
                 email = None,
                 token=None,
                 expo_push_token = None,
                 user_type = None,
                 relevant_id=None,
                 updated_at = None
                 ):
        self.relevant_id = relevant_id
        self.user_name = user_name
        self.shop_name = shop_name
        self.owner_name = owner_name
        self.owner_phone_no = owner_phone_no
        self.shop_phone_no1 = shop_phone_no1
        self.shop_phone_no2 = shop_phone_no2
        self.loc_long = loc_long
        self.loc_lat = loc_lat
        self.address = address
        self.password = password
        self.image = image
        self.email = email
        self.token = token
        self.expo_push_token = expo_push_token
        self.user_type = user_type
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def __repr__(self):
        return '<User %r>' % (self.name)

    def toDict(self):
        u = {
            "id": self.id,
            "user_name" : self.user_name,
            "shop_name" : self.shop_name,
            "owner_name" : self.owner_name,
            "owner_phone_no" : self.owner_phone_no,
            "shop_phone_no1" : self.shop_phone_no1,
            "shop_phone_no2" : self.shop_phone_no2,
            "loc_long" : self.loc_long,
            "loc_lat" : self.loc_lat,
            "address" : self.address,
            "image" : self.image,
            "email" : self.email,
            "token": self.token,
            "expo_push_token": self.expo_push_token,
            "user_type": self.user_type,
            "relevant_id": self.relevant_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
         }
        return u

    def toDict1(self):
        u = {
            "user_id": self.id,
            "user_name_shopkeeper" : self.user_name,
            "user_shop_name" : self.shop_name,
            "user_owner_name" : self.owner_name,
            "user_address" : self.address,
            "user_image" : self.image,
         }
        return u
