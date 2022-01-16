from flask_cors import CORS
from src.logic_processor.common import token_required
from src.logic_processor.user_accounts_processor import UAP
import json
from flask import (
    Blueprint, request)
from src.database.db import Session
Session.create_session()
from src.models.User import User
user_bp = Blueprint('user', __name__, url_prefix='/api/user')
CORS(user_bp)

@user_bp.route('/insert_user', methods=['POST'])
def process_register():
    res = UAP.process_register(request.json)
    return res

@user_bp.route("/update_user",methods=['POST'])
def update_user():
    return UAP.update_user(request.json)

@user_bp.route("/list_users",methods=['POST'])
def list_user():
    u = User.query.all()
    ul = [us.toDict() for us in u]
    return json.dumps(ul)

@user_bp.route("/login",methods=['POST'])
def login_user():
    return UAP.process_login(request.json)

@user_bp.route("/logout",methods=['POST'])
def logout_user():
    return UAP.process_logout(request.json)

@user_bp.route("/update_password",methods=['POST'])
@token_required
def update_password():
    return UAP.update_pass_shop(request.json)

@user_bp.route("/update_user_picture",methods=['GET','POST'])
def update_shop_picture():
    return UAP.update_user_picture(request.json)

@user_bp.route("/get_user_picture",methods=['GET','POST'])
def get_shop_picture():
    return UAP.get_user_picture(request.json)

@user_bp.route("/forgetPassword",methods=['POST'])
def forgetPassword():
    return UAP.forget_Password(request.json)

@user_bp.route("/resetPassword",methods=['GET'])
def resetPassword():
    return UAP.reset_password(request.json)

@user_bp.route("/addCustomer_Shopkeeper", methods=['POST'])
def add_Customer_Shopkeeper():
    return UAP.add_user_shopkeeper(request.json)

@user_bp.route("/removeCustomer_Shopkeeper", methods=['POST'])
def remove_Customer_Shopkeeper():
    return UAP.remove_user_shopkeeper(request.json);

@user_bp.route("/list/relevent/users", methods=['POST'])
def list_relevent_users():
    return UAP.list_relevent_users(request.json);

@user_bp.route("/customers/list", methods=['POST'])
def list_customers():
    return UAP.list_customers(request.json);

@user_bp.route("/notification/register", methods=['POST'])
def register_expo_notification():
    return UAP.register_expo_notifcation(request.json);

