import datetime
import json
from src.database.db import Session
from src.logic_processor.pushnotifications import send_push_message
Session.create_session()
db_session = Session.session.get_session()
engine = Session.session.get_engine()
from src.models.Products import Products
from src.models.Orders import Orders
from src.models.User import User
from src.logic_processor import common
import os

class OrdersProcessor:
    def process_insert_order(self, req):
        try:
            if not req:
                return common.make_response_packet('', None, 400, False, 'Invalid Data')

            if not 'product_id' in req:
                return common.make_response_packet('', None, 400, False, 'Product Id is required')

            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')

            if not 'quantities' in req:
                return common.make_response_packet('', None, 400, False, 'Quantities is required')

            user_id = req['user_id']
            product_id = req['product_id']
            quantities = req['quantities']
            total_price = req['total_price']

            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type !='customer':
                return common.make_response_packet('', None, 400, False, 'You are not customer')

            o = Orders(
                status="pending",
                quantities=quantities,
                total_price=total_price,
                user_id=user_id,
                product_id=product_id,
            )
            db_session.add(o)
            db_session.commit()
            # send_push_message(is_user_exist.expo_push_token, is_user_exist.user_name + "added new product " + product_name)
            return common.make_response_packet('Order successfully placed', o.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in process_insert_order", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")

        Session.session.destroy_session()

###############################################################################

    def list_orders(self, req):
        try:
            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')
            user_id = req['user_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            orders_data = []
            orders = db_session.query(Orders).filter(Products.user_id == user_id).all();
            for p in orders:
                resp = p.toDict()
                orders_data.append(resp)
            return common.make_response_packet('Orders Successfully Retrieved', orders_data, 200, True, '')

        except Exception as ex:
            print("Exception in list_orders", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()


###############################################################################

###############################################################################

    def update_order(self, req):
        try:
            if not req:
                return common.make_response_packet("", None, 400, False, "invalid data")
            if not 'order_id' in req:
                return common.make_response_packet("", None, 400, False, "order id is required")
            if not 'user_id' in req:
                return common.make_response_packet("", None, 400, False, "user id is required")

            user_id = req['user_id']
            order_id = req['order_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            pr = db_session.query(Orders).filter(Orders.id == order_id).first()
            if (not pr):
                return common.make_response_packet('', None, 400, False, 'invalid order id')
            keys = pr.__table__.columns
            updated = False
            for k in keys:
                updated |= common.check_and_update(pr, req, k.name)
            if (updated):
                pr.updated_at = datetime.datetime.now()
                db_session.commit()
                return common.make_response_packet('Order successfully updated', pr.toDict(), 200, True, '')
            else:
                return common.make_response_packet('Nothing Updated', pr.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in update_order", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

###############################################################################

    def get_product(self, req):
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
            prod = db_session.query(Products).filter(Products.id == product_id).first()
            resp = prod.toDict();
            target = os.path.abspath("static/")
            user_folder = os.path.join(target, is_user_exist.user_name)
            if not os.path.isdir(user_folder):
                resp['image1'] = ''
                resp['image2'] = ''
                resp['image3'] = ''
            else:
                product_folder = os.path.join(user_folder,"product_pic")
                if not os.path.isdir(product_folder):
                    resp['image1'] = ''
                    resp['image2'] = ''
                    resp['image3'] = ''
                else:
                    image1 = prod.image1 + ".png";
                    image2 = prod.image2 + ".png";
                    image3 = prod.image3 + ".png";
                    if not os.path.isfile(os.path.join(product_folder, image1)):
                        resp['image1'] = ''
                    else:
                        resp['image1'] = "static\\"+is_user_exist.user_name+"\\product_pic"+"\\"+image1;
                    if not os.path.isfile(os.path.join(product_folder, image2)):
                        resp['image2'] = ''
                    else:
                        resp['image2'] = "static\\"+is_user_exist.user_name+"\\product_pic"+"\\"+image2;
                    if not os.path.isfile(os.path.join(product_folder, image3)):
                        resp['image3'] = ''
                    else:
                        resp['image3'] = "static\\"+is_user_exist.user_name+"\\product_pic"+"\\"+image3;

            return common.make_response_packet('', resp, 200, True, '')

        except Exception as ex:
            print("Exception in delete_product", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

###############################################################################

    def delete_order(self, req):
        try:
            if not 'product_id' in req:
                return common.make_response_packet("", None, 400, False, "product id is required")
            if not 'user_id' in req:
                return common.make_response_packet("", None, 400, False, "user id is required")

            user_id = req['user_id']
            order_id = req['order_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')

            pr = db_session.query(Orders).filter(Orders.id == order_id).first()
            if pr:
                db_session.delete(pr)
                db_session.commit()
                return common.make_response_packet('Order successfully Deleted', None, 200, True, '')
            else:
                return common.make_response_packet('Nothing Deleted', None, 200, True, '')
        except Exception as ex:
            print("Exception in delete_order", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")
        Session.session.destroy_session()

###############################################################################

OP = OrdersProcessor()