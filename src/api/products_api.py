from flask_cors import CORS
from flask import (
    Blueprint, request
)
from src.logic_processor.product_processor import PP

products_pp = Blueprint('products', __name__, url_prefix='/api/product')
CORS(products_pp)

@products_pp.route('/insert',methods=['POST'])
def insert_product():
    res = PP.process_insert_product(request.json)
    return res

@products_pp.route("/list",methods=['POST'])
def list_products():
    return PP.list_products(request.json)

@products_pp.route('/update',methods=['POST'])
def update_product():
    return PP.update_product(request.json)

@products_pp.route('/delete',methods=['POST'])
def delete_product():
    return PP.delete_product(request.json)

@products_pp.route('/get',methods=['POST'])
def get_product():
    return PP.get_product(request.json)
