import base64
import uuid
from src.database.db import db_session
from src.models.ShopKeepers import ShopKeepers
from src.dto.UserType import UserType
from flask import session
from sqlalchemy import and_
from src.logic_processor import constants
from src.logic_processor import common
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserAccountsProcessor:

    def process_insert_shopkeeper(self,s):
        if(not s.user_name or not s.owner_name or  not s.shop_name or not s.password ):
            return common.make_response_packet(6, "Data is not valid", s.toDict())
        is_user_exist = ShopKeepers.query.filter(ShopKeepers.user_name == s.user_name).first() != None
        if(is_user_exist):
            return common.make_response_packet(7, "User name already in use", None)
        is_ownerphone_no_exist = ShopKeepers.query.filter(ShopKeepers.owner_phone_no == s.owner_phone_no).first() != None
        if (is_ownerphone_no_exist):
            return common.make_response_packet(7, "Phone number already in use", None)
        is_shop_name_exist = ShopKeepers.query.filter(ShopKeepers.shop_name == s.shop_name).first() != None
        if (is_shop_name_exist):
            return common.make_response_packet(7, "Shop name already in use", None)
        is_email_exist = ShopKeepers.query.filter(ShopKeepers.email == s.email).first() != None
        if (is_email_exist):
            return common.make_response_packet(7, "Email Already Exists", None)
        s.password=generate_password_hash(s.password)
        db_session.add(s)
        db_session.commit()
        return common.make_response_packet(0, "Shop keeper Inserted Successfully", s.toDict())


    def update_shopkeeper(self,s):
        authentic = common.is_user_authenticated()
        if (not authentic):
            return common.make_response_packet(4, "User is not authenticated", None)
        if (not s['shopkeeper_id']):
            return common.make_response_packet(5,'Shopkeeper id is required',None)
        shop = ShopKeepers.query.filter(ShopKeepers.id== s['shopkeeper_id']).first()
        if (not shop):
            return common.make_response_packet(6,'shopkeeper_id is not valid',None)

        keys = shop.__table__.columns
        updated =False
        for k in keys:
            updated |= common.check_and_update(shop,s,k.name)
        if(updated):
            is_shop_name_exist = ShopKeepers.query.filter(and_(ShopKeepers.shop_name == shop.shop_name,ShopKeepers.id != shop.id)).first() != None
            if (is_shop_name_exist):
                return common.make_response_packet(7, "Shop name already in use", None)
            db_session.commit()
            return common.make_response_packet(0, "Updated successfully", shop.toDict())
        else:
            return common.make_response_packet(1, 'Nothing Updated', shop.toDict())

    def update_shopkeeper_picture(self,s):
        authentic = common.is_user_authenticated()
        if (not authentic):
            return common.make_response_packet(4, "User is not authenticated", None)
        target = os.path.abspath("static/")
        if (not s['shopkeeper_id']):
            return common.make_response_packet(5, 'Shopkeeper id is required', None)
        shop = ShopKeepers.query.filter(ShopKeepers.id == s['shopkeeper_id']).first()
        if (not shop):
            return common.make_response_packet(6, 'shopkeeper_id is not valid', None)
        user_folder_create = os.path.join(target,shop.user_name)
        if not os.path.isdir(user_folder_create):
            os.mkdir(user_folder_create)
        user_profile_direc = os.path.join(user_folder_create,"profile_pics")
        if not os.path.isdir(user_profile_direc):
            os.mkdir(user_profile_direc)
        f = s['file_attachement']
        f = bytes(f, 'utf-8')
        filename = uuid.uuid1().hex
        shop.image = filename
        destination = "/".join([user_profile_direc, filename])
        print(destination)
        with open(destination + ".jpg", "wb") as fh:
            fh.write(base64.decodebytes(f))
        db_session.commit()
        return common.make_response_packet(1, 'Image Updated Successfully', 'Server Data')

    def get_shopkeeper_picture(self,s):
        authentic = common.is_user_authenticated()
        if (not authentic):
            return common.make_response_packet(4, "User is not authenticated", None)
        target = os.path.abspath("static/")
        if (not s['shopkeeper_id']):
            return common.make_response_packet(5, 'Shopkeeper id is required', None)
        shop = ShopKeepers.query.filter(ShopKeepers.id == s['shopkeeper_id']).first()
        if (not shop):
            return common.make_response_packet(6, 'shopkeeper_id is not valid', None)
        if shop.image:
            user_profile_direc = os.path.join(target, shop.user_name+"\profile_pics\\"+shop.image)
            print(target)
            print(user_profile_direc)
            with open(user_profile_direc + ".jpg", "rb") as image_file:
                my_string = base64.b64encode(image_file.read())
            return common.make_response_packet(1, 'success', my_string.decode('utf-8'))
        else:
            user_profile_direc = (target + "\\default.jpg")
            print(target)
            print(user_profile_direc)

            with open(user_profile_direc, "rb") as image_file:
                my_string = base64.b64encode(image_file.read())

            return common.make_response_packet(1, 'success', my_string.decode('utf-8'))

    def process_login(self,user_name,password,user_type):
        s = None
        if user_type == UserType.ShopKeeper:
            s = ShopKeepers.query.filter( ShopKeepers.user_name == user_name ).first()
        # elif user_type == UserType.Customer:
        #     s = Customers.query.filter(Customers.customer_name == user_name).first()
        else:
            return common.make_response_packet(1, "Not valid user type", None)

        if(s == None):
            return common.make_response_packet(2,  "User Name Not Found", None)
        if(not check_password_hash(s.password,password)):
            return common.make_response_packet(3, "User Name or Password is Incorrect", None)
        session[constants.is_authenticated] = True
        session[constants.user_type] = user_type
        return  common.make_response_packet(0,"Login Successfully",s.toDict())

    def process_logout(self):
        session[constants.is_authenticated] = None
        session[constants.user_type] = None
        return common.make_response_packet(0,"Logout Successfully",None)

    def update_pass_shop(self, s):
        authentic = common.is_user_authenticated()
        if (not authentic):
            return common.make_response_packet(4, "User is not authenticated", None)
        if (not 'user_name' in s):
            return common.make_response_packet(5, 'User name is required', None)
        shop = ShopKeepers.query.filter(ShopKeepers.user_name == s['user_name']).first()
        if (not shop):
            return common.make_response_packet(6, 'user_name is not valid', None)
        if('old_password' not in s or 'new_password' not in s):
            return common.make_response_packet(21,"Data is not valid",None)
        correct = check_password_hash(shop.password,s['old_password'])
        if correct:
            shop.password = generate_password_hash(s['new_password'])
            db_session.commit()
            return common.make_response_packet(0, "Password Updated Successfully", shop.toDict())
        else:
            return common.make_response_packet(1, 'Incorrect Old Password', shop.toDict())

UAP = UserAccountsProcessor()