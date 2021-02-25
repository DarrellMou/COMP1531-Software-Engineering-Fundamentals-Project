# need a dictionary to match credentials with actual reference(auth_user_id) 
from src.error import InputError 
import re

# temporary userinfo, the database
userinfo = {
    'adminemail@domain.com' : {'passwd' : '123456', 'auth_user_id' : '999'} # list or dictionary is ok, but not set
}

def auth_login_v1(email, password):				
    if(auth_email_format(email) == False):
        raise InputError
	
    for key in userinfo.keys():
    	if(email == key and password == userinfo[key]['passwd']):
            return userinfo[key]['auth_user_id'] # to do:what is {auth_id} ?			
    raise InputError

def auth_register_v1(email, password, name_first, name_last):
    return 1

# checks if email address has valid format, if so returns true
def auth_email_format(email):
    pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
	
    return bool(re.match(pattern, email))
