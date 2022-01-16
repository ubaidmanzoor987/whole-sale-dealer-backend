import datetime
import json

from src.database.db import Session
Session.create_session()
db_session = Session.session.get_session()
engine = Session.session.get_engine()
from src.models.Brands import Brands
from src.models.User import User
from src.logic_processor import common

class BrandsProcessor:
    def process_insert_brands(self, req):
        try:
            if not 'brand_name' in req:
                return common.make_response_packet('', None, 400, False, 'Brand Name is required')

            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User is required')

            user_id = req['user_id']
            brand_name = req['brand_name']
            own_brand = req['own_brand'] if 'own_brand' in req else False
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type !='shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')
            select_shop_keeper = db_session.query(Brands).filter(Brands.user_id == user_id).all()
            if select_shop_keeper:
                for i in range(len(select_shop_keeper)):
                    if brand_name == select_shop_keeper[i].brand_name:
                        return common.make_response_packet('', None, 400, False, 'Brand Name already exists')
            b = Brands(brand_name=brand_name,user_id=user_id, own_brand=own_brand)
            db_session.add(b)
            db_session.commit()
            return common.make_response_packet('Brand inserted successfully', b.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in proccess_insert_brand", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()
###############################################################################

    def get_brands(self, req):
        try:
            if not req:
                return common.make_response_packet('', None, 400, False, 'user_id is required, invalid data')
            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'user_id is required')
            user_id = req['user_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'you are not shopkeeper')
            brn = db_session.query(Brands).filter(Brands.user_id == user_id).all()
            brands_data = []
            if brn:
                for brands in brn:
                    brands_data.append({
                        'id': brands.id,
                        'brand_name': brands.brand_name,
                        'own_brand': brands.own_brand
                    })
                return common.make_response_packet('success', brands_data, 200, True, '')
            else:
                return common.make_response_packet('No Data', [], 200, True, '')
        except Exception as ex:
            print("Exception in get_brands", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

###############################################################################

    def update_brand(self, br):
        try:
            if not 'brand_id' in br:
                return common.make_response_packet("", None, 400, False, "brand id is required")
            if not 'user_id' in br:
                return common.make_response_packet("", None, 400, False, "user id is required")

            user_id = br['user_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            brn = db_session.query(Brands).filter(Brands.id == br['brand_id'] and Brands.user_id == user_id).first()
            if (not brn):
                return common.make_response_packet('', None, 400, False, 'invalid brand id')
            keys = brn.__table__.columns
            updated = False
            for k in keys:
                updated |= common.check_and_update(brn, br, k.name)
            if (updated):
                brn.updated_at = datetime.datetime.now()
                db_session.commit()
                return common.make_response_packet('Brand successfully updated', brn.toDict(), 200, True, '')
            else:
                return common.make_response_packet('Nothing Updated', brn.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in update_brand", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

###############################################################################

    def delete_brand(self, br):
        try:
            if not 'brand_id' in br:
                return common.make_response_packet("", None, 400, False, "brand id is required")
            if not 'user_id' in br:
                return common.make_response_packet("", None, 400, False, "user id is required")

            brn = db_session.query(Brands).filter(Brands.id == br['brand_id'] and Brands.user_id == br['user_id']).first()
            if (not brn):
                return common.make_response_packet("", None, 400, False, "brand id or user_id invalid")

            if brn:
                user_id = br['user_id']
                is_user_exist = db_session.query(User).filter(User.id == user_id).first()
                if not is_user_exist:
                    return common.make_response_packet('', None, 400, False, 'Invalid user id')
                elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                    return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')
                db_session.delete(brn)
                db_session.commit()
                return common.make_response_packet('Brand successfully Deleted', None, 200, True, '')
            else:
                return common.make_response_packet('Nothing Deleted', None, 200, True, '')
        except Exception as ex:
            print("Exception in delete_brand", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################
BPP = BrandsProcessor()