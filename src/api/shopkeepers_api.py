from flask_cors import CORS
from src.logic_processor.common import token_required
from src.logic_processor.user_accounts_processor import UAP
import json

from flask import (
    Blueprint, request)
from src.database.db import Session
Session.create_session()
from src.models.ShopKeepers import ShopKeepers
shopkeeper_bp = Blueprint('shopkeeper', __name__, url_prefix='/api/shopkeeper')
CORS(shopkeeper_bp)

@shopkeeper_bp.route('/insert_shopkeeper', methods=['POST'])
def insert_shop_keeper():
    res = UAP.process_insert_shopkeeper(request.json)
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
    return UAP.process_login(request.json)

@shopkeeper_bp.route("/logout",methods=['POST'])
def logout_shopkeeper():
    return UAP.process_logout(request.json)

@shopkeeper_bp.route("/update_password",methods=['POST'])
@token_required
def update_password():
    return UAP.update_pass_shop(request.json)

@shopkeeper_bp.route("/update_user_picture",methods=['GET','POST'])
def update_shop_picture():
    return UAP.update_shopkeeper_picture(request.json)

@shopkeeper_bp.route("/get_user_picture",methods=['GET','POST'])
def get_shop_picture():
    return UAP.get_shopkeeper_picture(request.json)
@shopkeeper_bp.route("/forgetPassword",methods=['POST'])

def forgetPassword():
    return UAP.forget_Password(request.json)
@shopkeeper_bp.route("/resetPassword",methods=['GET'])
def resetPassword():
    return UAP.reset_password(request.json)

