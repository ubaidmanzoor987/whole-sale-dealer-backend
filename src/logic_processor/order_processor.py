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

            if not 'product' in req:
                return common.make_response_packet('', None, 400, False, 'Product data is required')

            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')

            user_id = req['user_id']
            product = req['product']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type !='customer':
                return common.make_response_packet('', None, 400, False, 'You are not customer')

            orders_data = [];
            for prod in product:
                id = prod['id'];
                quant = prod['quantity'];
                total_price = prod['total_price'];
                o = Orders(
                    status="pending",
                    quantites=quant,
                    total_price=total_price,
                    user_id=user_id,
                    product_id=id,
                )
                p = db_session.query(Products).filter(Products.id == id).first()
                orders_data.append(o.toDict())
                if p.quantities > 0:
                    new_quantity = p.quantities - quant;
                    p.quantities = new_quantity
                    db_session.add(p)
                db_session.add(o)
            db_session.commit()
            Session.session.destroy_session()
            # send_push_message(is_user_exist.expo_push_token, is_user_exist.user_name + "added new product " + product_name)
            return common.make_response_packet('Order successfully placed', orders_data, 200, True, '')
        except Exception as ex:
            print("Exception in process_insert_order", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")


###############################################################################
    def convert_img_to_b64(self, imagePath):
        try:
            import base64
            with open(imagePath, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read())
                return b64_string.decode('utf-8');
        except Exception as ex:
            print("Exception in convert img to b64", ex);
            return "";

    def list_orders(self, req):
        try:
            if not 'user_id' in req:
                return common.make_response_packet('', None, 400, False, 'User id is required')
            user_id = req['user_id']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            orders_data = []
            target = os.path.abspath("static/")
            if is_user_exist.user_type == "customer":
                orders = db_session.query(Orders).filter(Orders.user_id == user_id).all();
                for order in orders:
                    resp = order.toDict()
                    user_name = order.product_rel.shopkeeper_rel.user_name;
                    user_folder = os.path.join(target, user_name)
                    if not os.path.isdir(user_folder):
                        resp['image1'] = ''
                        resp['image2'] = ''
                        resp['image3'] = ''
                    else:
                        product_folder = os.path.join(user_folder, "product_pic")
                        if not os.path.isdir(product_folder):
                            resp['image1'] = ''
                            resp['image2'] = ''
                            resp['image3'] = ''
                            resp["image1b64"] = ''
                            resp["image2b64"] = ''
                            resp["image3b64"] = ''
                        else:
                            image1 = resp["image1"] + ".png" if "image1" in resp else "";
                            image2 = resp["image2"] + ".png" if "image2" in resp else "";
                            image3 = resp["image3"] + ".png" if "image3" in resp else "";
                            if not os.path.isfile(os.path.join(product_folder, image1)):
                                resp['image1'] = ''
                                resp["image1b64"] = ''
                            else:
                                resp[
                                    'image1'] = "static\\" + user_name + "\\product_pic" + "\\" + image1;
                                resp["image1b64"] = self.convert_img_to_b64(os.path.join(product_folder, image1))
                            if not os.path.isfile(os.path.join(product_folder, image2)):
                                resp['image2'] = ''
                                resp["image2b64"] = ''
                            else:
                                resp[
                                    'image2'] = "static\\" + user_name + "\\product_pic" + "\\" + image2;
                                resp["image2b64"] = self.convert_img_to_b64(os.path.join(product_folder, image2))
                            if not os.path.isfile(os.path.join(product_folder, image3)):
                                resp['image3'] = ''
                                resp["image3b64"] = ''
                            else:
                                resp[
                                    'image3'] = "static\\" + user_name + "\\product_pic" + "\\" + image3;
                                resp["image3b64"] = self.convert_img_to_b64(os.path.join(product_folder, image3))
                    orders_data.append(resp)
                return common.make_response_packet('Orders Successfully Retrieved', orders_data, 200, True, '')
            else:
                all_orders = db_session.query(Orders).all();
                for order in all_orders:
                    resp = order.toDict()
                    product_rel = order.product_rel;
                    shop_keeper_id = product_rel.user_id;
                    if (user_id == shop_keeper_id):
                        user_name = product_rel.shopkeeper_rel.user_name;
                        user_folder = os.path.join(target, user_name)
                        if not os.path.isdir(user_folder):
                            resp['image1'] = ''
                            resp['image2'] = ''
                            resp['image3'] = ''
                        else:
                            product_folder = os.path.join(user_folder, "product_pic")
                            if not os.path.isdir(product_folder):
                                resp['image1'] = ''
                                resp['image2'] = ''
                                resp['image3'] = ''
                                resp["image1b64"] = ''
                                resp["image2b64"] = ''
                                resp["image3b64"] = ''
                            else:
                                image1 = resp["image1"] + ".png" if "image1" in resp else "";
                                image2 = resp["image2"] + ".png" if "image2" in resp else "";
                                image3 = resp["image3"] + ".png" if "image3" in resp else "";
                                if not os.path.isfile(os.path.join(product_folder, image1)):
                                    resp['image1'] = ''
                                    resp["image1b64"] = ''
                                else:
                                    resp[
                                        'image1'] = "static\\" + user_name + "\\product_pic" + "\\" + image1;
                                    resp["image1b64"] = self.convert_img_to_b64(os.path.join(product_folder, image1))
                                if not os.path.isfile(os.path.join(product_folder, image2)):
                                    resp['image2'] = ''
                                    resp["image2b64"] = ''
                                else:
                                    resp[
                                        'image2'] = "static\\" + user_name + "\\product_pic" + "\\" + image2;
                                    resp["image2b64"] = self.convert_img_to_b64(os.path.join(product_folder, image2))
                                if not os.path.isfile(os.path.join(product_folder, image3)):
                                    resp['image3'] = ''
                                    resp["image3b64"] = ''
                                else:
                                    resp[
                                        'image3'] = "static\\" + user_name + "\\product_pic" + "\\" + image3;
                                    resp["image3b64"] = self.convert_img_to_b64(os.path.join(product_folder, image3))
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
            status = req['status']
            is_user_exist = db_session.query(User).filter(User.id == user_id).first()
            if not is_user_exist:
                return common.make_response_packet('', None, 400, False, 'Invalid user id')
            elif is_user_exist and is_user_exist.user_type != 'shop_keeper':
                return common.make_response_packet('', None, 400, False, 'You are not shopkeeper')

            pr = db_session.query(Orders).filter(Orders.id == order_id).first()
            if (not pr):
                return common.make_response_packet('', None, 400, False, 'invalid order id')
            pr.status = status;
            pr.updated_at = datetime.datetime.now()
            db_session.add(pr)
            db_session.commit()
            Session.session.destroy_session()
            return common.make_response_packet('Order successfully updated', pr.toDict(), 200, True, '')
            # keys = pr.__table__.columns
            # updated = False
            # for k in keys:
            #     updated |= common.check_and_update(pr, req, k.name)
            # if (updated):
            # else:
            #     return common.make_response_packet('Nothing Updated', pr.toDict(), 200, True, '')
        except Exception as ex:
            print("Exception in update_order", ex)
            return common.make_response_packet("", None, 400, False, "Server Error")

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