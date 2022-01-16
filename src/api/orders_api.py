from flask_cors import CORS
from flask import (
    Blueprint, request
)
from src.logic_processor.order_processor import OP

orders_pp = Blueprint('orders', __name__, url_prefix='/api/order')
CORS(orders_pp)

@orders_pp.route('/insert',methods=['POST'])
def insert_order():
    res = OP.process_insert_order(request.json)
    return res

@orders_pp.route("/list",methods=['POST'])
def list_orders():
    return OP.list_orders(request.json)

@orders_pp.route('/update',methods=['POST'])
def update_order():
    return OP.update_order(request.json)

@orders_pp.route('/delete',methods=['POST'])
def delete_order():
    return OP.delete_order(request.json)
