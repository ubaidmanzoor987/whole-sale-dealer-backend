import json

from src.database.db import Session
Session.create_session()
db_session = Session.session.get_session()
engine = Session.session.get_engine()
from src.models.Products import Products
from src.models.User import User
from src.models.Brands import Brands
from src.logic_processor import common
import os
from PIL import Image
from io import BytesIO
from base64 import b64decode
import base64
import datetime
import uuid

class ProductsProcessor:
    def process_insert_product(self, req):
        try:
            if not 'product_name' in req:
                return common.make_response_packet('', None, 400, False, 'Product Name is required')

            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')

            if not 'brand_id' in req:
                return common.make_response_packet('', None, 400, False, 'Brand id is required')

            if not 'price' in req:
                return common.make_response_packet('', None, 400, False, 'Price is required')

            if not 'quantities' in req:
                return common.make_response_packet('', None, 400, False, 'Quantities is required')

            user_id = req['user_id']
            brand_id = req['brand_id']
            product_name = req['product_name']
            product_des = req['product_des'] if 'product_des' in req else ''
            image1 = req['image1'] if 'image1' in req else ''
            image2 = req['image2'] if 'image2' in req else ''
            image3 = req['image3'] if 'image3' in req else ''
            price = req['price']
            quantities = req['quantities']

            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type !='shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            #Save Image
            if image1 != '':
                target = os.path.abspath("static/")
                user_folder_create = os.path.join(target, is_user_exist.user_name)
                if not os.path.isdir(user_folder_create):
                    os.mkdir(user_folder_create)
                user_product_direc = os.path.join(user_folder_create, "product_pic")
                if not os.path.isdir(user_product_direc):
                    os.mkdir(user_product_direc)
                f = image1
                im = Image.open(BytesIO(b64decode(f.split(',')[1])))
                filename = uuid.uuid1().hex
                destination = "\\".join([user_product_direc, filename])
                im.save(destination + ".png")
                image1 = filename

            if image2 != '':
                target = os.path.abspath("static/")
                user_folder_create = os.path.join(target, is_user_exist.user_name)
                if not os.path.isdir(user_folder_create):
                    os.mkdir(user_folder_create)
                user_product_direc = os.path.join(user_folder_create, "product_pic")
                if not os.path.isdir(user_product_direc):
                    os.mkdir(user_product_direc)
                f = image2
                im = Image.open(BytesIO(b64decode(f.split(',')[1])))
                filename = uuid.uuid1().hex
                destination = "\\".join([user_product_direc, filename])
                im.save(destination + ".png")
                image2 = filename

            if image3 != '':
                target = os.path.abspath("static/")
                user_folder_create = os.path.join(target, is_user_exist.user_name)
                if not os.path.isdir(user_folder_create):
                    os.mkdir(user_folder_create)
                user_product_direc = os.path.join(user_folder_create, "product_pic")
                if not os.path.isdir(user_product_direc):
                    os.mkdir(user_product_direc)
                f = image3
                im = Image.open(BytesIO(b64decode(f.split(',')[1])))
                filename = uuid.uuid1().hex
                destination = "\\".join([user_product_direc, filename])
                im.save(destination + ".png")
                image3 = filename

            p = Products(
                product_name=product_name,
                brand_id=brand_id,
                product_des=product_des,
                user_id=user_id,
                image1=image1,
                image2=image2,
                image3=image3,
                price=price,
                quantities=quantities
            )
            db_session.add(p)
            db_session.commit()
            return common.make_response_packet('Product inserted successfully', p.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in proccess_insert_brand", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")

        Session.session.destroy_session()
###############################################################################

    def list_products_shopkeeper(self, req):
        try:
            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')

            user_id = req['user_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist.user_type != "shop_keeper":
                return common.make_response_packet('', None, 400, False, 'Not a shopkeeper')
            products = db_session.query(Products).filter(Products.shopkeeper_id == user_id).all()
            products_data = []
            for p in products:
                products_data.append(p.toDict())
            return common.make_response_packet('success', products_data, 200, True, '')

        except Exception as ex:
            print("Exception in get_products", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()


###############################################################################

###############################################################################

    def update_product(self, req):
        try:
            if not 'product_id' in req:
                return common.make_response_packet("", None, 400, False, "product id is required")
            if not 'user_id' in req:
                return common.make_response_packet("", None, 400, False, "user id is required")

            user_id = req['user_id']
            product_id = req['product_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            pr = db_session.query(Products).filter(Products.id == product_id).first()
            if (not pr):
                return common.make_response_packet('', None, 400, False, 'invalid product id')
            keys = pr.__table__.columns
            updated = False
            for k in keys:
                updated |= common.check_and_update(pr, req, k.name)
            if (updated):
                db_session.commit()
                return common.make_response_packet('Product successfully updated', pr.toDict(), 200, True, '')
            else:
                return common.make_response_packet('Nothing Updated', pr.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in update_product", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

###############################################################################

    def delete_product(self, req):
        try:
            if not 'product_id' in req:
                return common.make_response_packet("", None, 400, False, "product id is required")
            if not 'user_id' in req:
                return common.make_response_packet("", None, 400, False, "user id is required")

            user_id = req['user_id']
            product_id = req['product_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            pr = db_session.query(Products).filter(Products.id == product_id).first()
            if pr:
                db_session.delete(pr)
                db_session.commit()
                return common.make_response_packet('Product successfully Deleted', None, 200, True, '')
            else:
                return common.make_response_packet('Nothing Deleted', None, 200, True, '')
        except Exception as ex:
            print("Exception in delete_product", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################
PP = ProductsProcessor()