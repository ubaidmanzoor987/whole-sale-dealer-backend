from flask_cors import CORS
from src.logic_processor.user_accounts_processor import UAP
import json
from src.dto.UserType import UserType

from flask import (
    Blueprint, request
)
from src.models.ShopKeepers import ShopKeepers
shopkeeper_bp = Blueprint('shopkeeper', __name__, url_prefix='/api/shopkeeper')
CORS(shopkeeper_bp)

@shopkeeper_bp.route('/insert_shopkeeper',methods=['POST'])
def insert_shop_keeper():
    user_name = request.json.get('user_name')
    shop_name = request.json.get('shop_name')
    owner_name = request.json.get('owner_name')
    owner_phone_no = request.json.get('owner_phone_no')
    password = request.json.get('password')
    address = request.json.get('address')
    shop_phone_no1 = request.json.get('shop_phone_no1')
    shop_phone_no2 = request.json.get('shop_phone_no2')
    loc_long = request.json.get('loc_long')
    loc_lat = request.json.get('loc_lat')
    image = request.json.get('image')
    email  = request.json.get('email')
    s = ShopKeepers(user_name,shop_name,password,owner_name,owner_phone_no,shop_phone_no1,shop_phone_no2,loc_long,loc_lat,address,image,email)
    res = UAP.process_insert_shopkeeper(s)
    return res

@shopkeeper_bp.route("/update_shopkeeper",methods=['POST'])
def update_shopkeeper():
    return UAP.update_shopkeeper(request.json)

@shopkeeper_bp.route("/list_shopkeepers",methods=['POST'])
def list_shopkeeper():
    u = ShopKeepers.query.all()
    ul = [us.toDict() for us in u]
    return json.dumps(ul)

@shopkeeper_bp.route("/login",methods=['POST'])
def login_shopkeeper():
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    return UAP.process_login(user_name,password,UserType.ShopKeeper)

@shopkeeper_bp.route("/logout",methods=['POST'])
def logout_shopkeeper():
    return UAP.process_logout()

@shopkeeper_bp.route("/update_password",methods=['POST'])
def update_password():
    return UAP.update_pass_shop(request.json)

@shopkeeper_bp.route("/update_user_picture",methods=['GET','POST'])
def update_shop_picture():
    return UAP.update_shopkeeper_picture(request.json)

@shopkeeper_bp.route("/get_user_picture",methods=['GET','POST'])
def get_shop_picture():
    return UAP.get_shopkeeper_picture(request.json)


