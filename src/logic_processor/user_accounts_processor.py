import base64
import datetime
import uuid
import jwt
from src.database.db import Session
Session.create_session()
db_session = Session.session.get_session()
engine = Session.session.get_engine()
from src.models.ShopKeepers import ShopKeepers
from src.dto.UserType import UserType
from flask import session
from sqlalchemy import and_
from src.logic_processor import constants
from src.logic_processor import common
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserAccountsProcessor:

    ################################### Login Start ###########################################
    def process_login(self, req):
        if not 'user_name' in req:
            return common.make_response_packet('User Name is required', None, 202)

        if not 'password' in req:
            return common.make_response_packet('Password is required', None, 202)

        if not 'user_type' in req:
            return common.make_response_packet('User Type is required', None, 202)

        user_name = req['user_name']
        password = req['password']
        user_type = req['user_type']

        s = None
        if user_type == 'shop_keeper':
            s = ShopKeepers.query.filter( ShopKeepers.user_name == user_name ).first()
        else:
            return common.make_response_packet("Not valid user type", None, 400)

        if s is None:
            return common.make_response_packet('Incorrect User Name', None, 400)

        if(not check_password_hash(s.password, password)):
            return common.make_response_packet("User Name or Password is Incorrect", None, 201)

        env_variables = common.get_environ_variables()
        token = jwt.encode(
            {'user_name': s.user_name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            env_variables['SECRET_KEY'], "HS256")
        s.jwt_token = token
        db_session.add(s)
        db_session.commit()
        Session.session.destroy_session()
        return common.make_response_packet("Login Successfully", s.toDict())

    ################################### Login End ###########################################

    ################################### Logout Start ###########################################
    def process_logout(self, req):
        if not 'user_name' in req:
            return common.make_response_packet('User Name is required', None, 201)
        if not 'user_type' in req:
            return common.make_response_packet('User Type is required', None, 201)

        user_name = req['user_name']
        user_type = req['user_type']

        s = None
        if user_type == 'shop_keeper':
            s = ShopKeepers.query.filter( ShopKeepers.user_name == user_name ).first()
        else:
            return common.make_response_packet("Not valid user type", None, 403)

        if s is None:
            return common.make_response_packet('Incorrect User Name', None, 403)

        s.jwt_token = None
        db_session.add(s)
        db_session.commit()
        Session.session.destroy_session()
        return common.make_response_packet("Logout Successfully")

    ################################### Logout End ###########################################

    ################################### Insert Shopkeeper Start ###########################################
    def process_insert_shopkeeper(self,req):
        if not 'user_name' in req:
            return common.make_response_packet('User Name is required', None, 202)

        if not 'shop_name' in req:
            return common.make_response_packet('ShopName is required', None, 202)

        if not 'email' in req:
            return common.make_response_packet('Email is required', None, 202)

        if not 'password' in req:
            return common.make_response_packet('Password is required', None, 202)

        if not 'user_type' in req:
            return common.make_response_packet('User Type is required', None, 202)

        user_name = req['user_name']
        shop_name = req['shop_name']
        password = req['password']
        email = req['email']
        user_type = req['user_type']

        is_user_exist = ShopKeepers.query.filter(ShopKeepers.user_name == user_name).first() != None
        if(is_user_exist):
            return common.make_response_packet("User name already exists", None, 202)

        is_email_exist = ShopKeepers.query.filter(ShopKeepers.email == email).first() != None
        if (is_email_exist):
            return common.make_response_packet("Email Already Exists", None, 202)
        password = generate_password_hash(password)
        s = ShopKeepers(user_name=user_name, shop_name=shop_name, password=password, user_type=user_type)
        db_session.add(s)
        db_session.commit()
        Session.session.destroy_session()

        return common.make_response_packet("Shop keeper Inserted Successfully", None, 200)

    ###################################Insert Shopkeeper End ###########################################

    ################################### Update Shopkeeper Start ###########################################
    def update_shopkeeper(self,s):

        if (not s['user_name']):
            return common.make_response_packet('User Name is required', None, 403)
        shop = ShopKeepers.query.filter(ShopKeepers.user_name== s['user_name']).first()

        if (not shop):
            return common.make_response_packet('Invalid User Name', None, 403)

        keys = shop.__table__.columns
        updated =False
        for k in keys:
            updated |= common.check_and_update(shop,s,k.name)

        if(updated):
            is_shop_name_exist = ShopKeepers.query.filter(and_(ShopKeepers.shop_name == shop.shop_name,ShopKeepers.id != shop.id)).first() != None
            if (is_shop_name_exist):
                return common.make_response_packet("Shop name already in use", None, 403)

            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet("Updated successfully", shop.toDict())

        else:
            return common.make_response_packet('Nothing Updated', shop.toDict())

    ################################### Update Shopkeeper End ###########################################

    ################################### Update Shopkeeper Picture Start ###########################################
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

    ################################### Update Shopkeeper Picture End ###########################################

    ################################### Get Shopkeeper Picture Start ###########################################
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

    ################################### Get Shopkeeper Picture End ###########################################

    ################################### Update Shopkeeper Password Start ###########################################
    def update_pass_shop(self, s):
        if (not 'user_name' in s):
            return common.make_response_packet(200, 'User Name is required', None)

        shop = ShopKeepers.query.filter(ShopKeepers.user_name == s['user_name']).first()
        if (not shop):
            return common.make_response_packet(200, 'Invalid UserName', None)

        if not 'old_password' in s:
            return common.make_response_packet(200, 'Old Password is Required', None)

        if not 'new_password' in s:
            return common.make_response_packet(200, 'New Password is Required', None)

        correct = check_password_hash(shop.password, s['old_password'])
        if correct:
            shop.password = generate_password_hash(s['new_password'])
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet(200, "Password Updated Successfully", shop.toDict())
        else:
            return common.make_response_packet(200, 'Incorrect Old Password', None)

    ################################### Update Shopkeeper Password End ###########################################

UAP = UserAccountsProcessor()