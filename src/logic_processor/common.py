from flask import session
from src.logic_processor import constants
import json
from src.dto.UserType import UserType

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

def make_response_packet(status, error_message, data):
    s = {"status": status, "msg":error_message, "data": data}
    return json.dumps(s)


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
