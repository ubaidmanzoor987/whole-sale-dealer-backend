from functools import wraps
import jwt
from flask import session, make_response, request, jsonify
from src.logic_processor import constants
from src.dto.UserType import UserType
from dotenv import dotenv_values
config = dotenv_values(".env")

def is_user_authenticated():
    return True
    if(constants.is_authenticated in session):
        if(session[constants.is_authenticated] == True):
            return True
    return False

def is_shopkeeper():
    if(session[constants.user_type] != None):
        if(session[constants.user_type] == UserType.ShopKeeper):
            return True
    return False

def is_customer():
    if(session[constants.user_type] != None):
        if(session[constants.user_type] == UserType.Customer):
            return True
    return False

def make_response_packet(message='', data=None, status=200):
    return make_response({'message': message, 'data': data}, status)

def is_number(num):
    try:
        n = float(num)
        return True
    except:
        return False

def check_and_update(old_obj, new_obj, attr):
    if(not attr in new_obj):
        return False
    if(getattr(old_obj,attr) == new_obj[attr]):
        return False
    setattr(old_obj,attr,new_obj[attr])
    return True

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'A valid token is missing'})
        try:
            from src.database.db import Session
            from src.models.ShopKeepers import ShopKeepers
            data = jwt.decode(token, config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as ex:
            return jsonify({'message': str(ex)})

        return f(*args, **kwargs)

    return decorator

def get_environ_variables():
    try:
        from dotenv import dotenv_values
        config = dotenv_values(".env")
        return config
    except Exception as ex:
        print("Exception in get environment variables", ex)