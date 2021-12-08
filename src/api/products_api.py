from flask_cors import CORS
from flask import (
    Blueprint, request
)
from src.logic_processor.product_processor import PP

products_pp = Blueprint('products', __name__, url_prefix='/api/product')
CORS(products_pp)

@products_pp.route('/shopkeeper/insert',methods=['POST'])
def insert_brands():
    res = PP.process_insert_product(request.json)
    return res

@products_pp.route("/shopkeeper/list",methods=['POST'])
def list_brands():
    return PP.list_products_shopkeeper(request.json)

@products_pp.route('/shopkeeper/update',methods=['POST'])
def update_brand():
    return PP.update_product(request.json)

@products_pp.route('/shopkeeper/delete',methods=['POST'])
def delete_brand():
    return PP.delete_product(request.json)
