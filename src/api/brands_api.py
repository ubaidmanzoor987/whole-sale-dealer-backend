from flask_cors import CORS
from flask import (
    Blueprint, request
)
from src.logic_processor.brands_processor import BPP

brands_bp = Blueprint('brands', __name__, url_prefix='/api/brands')
CORS(brands_bp)

@brands_bp.route('/insert_brand',methods=['POST'])
def insert_brands():
    res = BPP.process_insert_brands(request.json)
    return res

@brands_bp.route("/list_brands",methods=['POST'])
def list_brands():
    return BPP.get_brands(request.json)

@brands_bp.route('/update_brand',methods=['POST'])
def update_brand():
    return BPP.update_brand(request.json)

@brands_bp.route('/delete_brand',methods=['POST'])
def delete_brand():
    return BPP.delete_brand(request.json)




