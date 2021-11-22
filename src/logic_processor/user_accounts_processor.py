import base64
import datetime
import uuid
import jwt
from src.database.db import Session
Session.create_session()
db_session = Session.session.get_session()
engine = Session.session.get_engine()
from src.models.User import User
from sqlalchemy import and_
from src.logic_processor import common
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserAccountsProcessor:

    ################################### Login Start ###########################################
    def process_login(self, req):
        try:
            if not 'user_name' in req:
                return common.make_response_packet('', None, 400, False, 'User Name is required')

            if not 'password' in req:
                return common.make_response_packet('', None, 400, False, 'Password is required')

            if not 'user_type' in req:
                return common.make_response_packet('', None, 400, False, 'User Type is required')

            user_name = req['user_name']
            password = req['password']
            user_type = req['user_type']

            s = None
            if user_type == 'shop_keeper':
                s = User.query.filter( User.user_name == user_name ).first()
            else:
                return common.make_response_packet('', None, 400, False, 'Not valid user type')

            if s is None:
                return common.make_response_packet('', None, 400, False, 'Incorrect User Name')

            if(not check_password_hash(s.password, password)):
                return common.make_response_packet('', None, 400, False, 'Incorect username or password')

            env_variables = common.get_environ_variables()
            token = jwt.encode(
                {'user_name': s.user_name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                env_variables['SECRET_KEY'], "HS256")
            s.token = token
            db_session.add(s)
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet("Login Successfully", s.toDict(), 200, True, None)
        except Exception as ex:
            print("Exception in process_login ", ex)
            return common.make_response_packet('', None, 400, False, 'Server Error' + ex.Message)

    ################################### Login End ###########################################

    ################################### Logout Start ###########################################
    def process_logout(self, req):
        try:
            if not 'user_name' in req:
                return common.make_response_packet('User Name is required', None, 400, False, None)
            if not 'user_type' in req:
                return common.make_response_packet('User Type is required', None, 400, False, None)

            user_name = req['user_name']
            user_type = req['user_type']

            s = None
            if user_type == 'shop_keeper':
                s = User.query.filter( User.user_name == user_name ).first()
            else:
                return common.make_response_packet("Not valid user type", None, 400, False, None)

            if s is None:
                return common.make_response_packet("Incorrect User Name", None, 400, False, None)
            s.token = None
            db_session.add(s)
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet("Logout Successfully", None, 200, True, None)
        except Exception as ex:
            print("Exception in process_logout", ex)
            return common.make_response_packet("Server Error", None, 400, False, ex)

    ################################### Logout End ###########################################

    ################################### Insert Shopkeeper Start ###########################################
    def process_register(self,req):
        try:
            if not 'user_name' in req:
                return common.make_response_packet('', None, 400, False, 'User Name is required')

            if not 'shop_name' in req:
                return common.make_response_packet('', None, 400, False, 'ShopName is required')

            if not 'email' in req:
                return common.make_response_packet('', None, 400, False, 'Email is required')

            if not 'password' in req:
                return common.make_response_packet('', None, 400, False, 'Password is required')

            if not 'user_type' in req:
                return common.make_response_packet('', None, 400, False, 'User Type is required')

            user_name = req['user_name']
            shop_name = req['shop_name']
            password = req['password']
            email = req['email']
            user_type = req['user_type']

            is_user_exist = User.query.filter(User.user_name == user_name).first() != None
            if(is_user_exist):
                return common.make_response_packet('', None, 400, False, 'User name already exists')

            is_email_exist = User.query.filter(User.email == email).first() != None
            if (is_email_exist):
                return common.make_response_packet('', None, 400, False, 'Email Already Exists')

            password = generate_password_hash(password)
            s = User(user_name=user_name, shop_name=shop_name, password=password, user_type=user_type)
            db_session.add(s)
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet("Shop keeper Inserted Successfully", s.toDict(), 200, True, None)
        except Exception as ex:
            print("Exception in proccess_signup", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")

    ###################################Insert Shopkeeper End ###########################################

    ################################### Update Shopkeeper Start ###########################################
    def update_shopkeeper(self,s):
        try:
            if (not s['user_name']):
                return common.make_response_packet('', None, 400, False, 'User Name is required')
            shop = User.query.filter(User.user_name== s['user_name']).first()

            if (not shop):
                return common.make_response_packet('', None, 400, False, 'Invalid User Name')

            keys = shop.__table__.columns
            updated =False
            for k in keys:
                updated |= common.check_and_update(shop,s,k.name)

            if(updated):
                is_shop_name_exist = User.query.filter(and_(User.shop_name == shop.shop_name,User.id != shop.id)).first() != None
                if (is_shop_name_exist):
                    return common.make_response_packet("", None, 400, False, 'Shop name already in use')

                db_session.commit()
                Session.session.destroy_session()
                return common.make_response_packet("Updated successfully", shop.toDict(), 200, True, None)

            else:
                return common.make_response_packet('Already Uptodate', shop.toDict(), 200, True, None)

        except Exception as ex:
            print("Excprption in update_user", ex)
            return common.make_response_packet('', None, 400, False, 'Server Error')
    ################################### Update Shopkeeper End ###########################################

    ################################### Update Shopkeeper Picture Start ###########################################
    def update_shopkeeper_picture(self,s):
        authentic = common.is_user_authenticated()
        if (not authentic):
            return common.make_response_packet(4, "User is not authenticated", None)
        target = os.path.abspath("static/")
        if (not s['shopkeeper_id']):
            return common.make_response_packet(5, 'Shopkeeper id is required', None)
        shop = User.query.filter(User.id == s['shopkeeper_id']).first()
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
        shop = User.query.filter(User.id == s['shopkeeper_id']).first()
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
            return common.make_response_packet('', None, 400, False, 'User Name is required')

        shop = User.query.filter(User.user_name == s['user_name']).first()
        if (not shop):
            return common.make_response_packet('', None, 400, False, 'Invalid UserName')

        if not 'old_password' in s:
            return common.make_response_packet('', None, 400, False, 'Old Password is Required')

        if not 'new_password' in s:
            return common.make_response_packet('', None, 400, False, 'New Password is Required')

        correct = check_password_hash(shop.password, s['old_password'])
        if correct:
            shop.password = generate_password_hash(s['new_password'])
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet('Password Updated Successfully', shop.toDict() , 200, True, None)

        else:
            return common.make_response_packet('', None, 400, False, 'Incorrect Old Password')

    ################################### Update Shopkeeper Password End ###########################################

    ################################### Foget Password start #####################################################
    def forget_Password(self, s):
        if(not 'email' in s):
            return common.make_response_packet('', None, 400, False, 'Email is required')
        email = s['email']
        user = User.query.filter(User.email == email).first();
        if user and user.user_name:
            return common.make_response_packet('User Found', user.toDict(), 200, False, None)
        else:
            return common.make_response_packet('', None, 400, False, 'Not found')

    ################################### Foget Password End #####################################################
    ################################### Reset Password start #####################################################
    def reset_password(self, s):
        if (not 'email' in s):
            return common.make_response_packet('', None, 400, False, 'Email is Required')
        if (not 'password' in s):
            return common.make_response_packet('', None, 400, False, 'Password is Required')
        if (not 'confirm_password' in s):
            return common.make_response_packet('', None, 400, False, 'Confirm Password is Required')
        if (s['passowrd'] != s['confirm_password']):
            return common.make_response_packet('', None, 400, False, 'Password is not matched')

        email = s['email'];
        password = s['password'];

        user = User.query.filter(User.email == email).first()

        user.password = generate_password_hash(password);
        db_session.add(user);
        db_session.commit();
        return common.make_response_packet('Password updated Successfully', user.toDict(), 200, False, None)

    ################################### Reset Password End #####################################################

UAP = UserAccountsProcessor()