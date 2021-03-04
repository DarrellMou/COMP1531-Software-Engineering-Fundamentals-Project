# need a dictionary to match credentials with actual reference(auth_user_id) 
from src.error import InputError 
from src.data import data
import re
import itertools
import uuid

# temporary userinfo, the database
userinfo = {
    'adminemail@domain.com' : {'passwd' : '123456', 'handle' : 'ahandle', 'auth_user_id' : '999'} # list or dictionary is ok, but not set
}

# checks if email address has valid format, if so returns true
def auth_email_format(email):
    pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
	
    return bool(re.match(pattern, email))

def auth_login_v1(email, password):				
    if(auth_email_format(email) == False):
        raise InputError
	
    for key in userinfo.keys():
    	if(email == key and password == userinfo[key]['passwd']):
            return {'auth_user_id' : int(userinfo[key]['auth_user_id'])} # to do:what is {auth_id} ?			
    raise InputError

def auth_register_v1(email, password, name_first, name_last):
    if(auth_email_format(email) == False):
        raise InputError
    elif(email in userinfo.keys()):
        raise InputError
    elif(len(password) < 6):
        raise InputError
    elif(len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1):
        raise InputError
    
    # generate handle and add to userinfo
    new_handle = name_first.lower() + name_last.lower()
    if len(new_handle) > 20:
        new_handle = new_handle[0:19]

    new_auth_user_id = int(uuid.uuid4()) # TODO: find a new way to generate 

    new_u_id = int(uuid.uuid4())

    if(any(new_handle == data['users'][user]['handle_str'] for user in data['users'])):
        for epilogue in itertools.count(0, 1):
            if(not any((new_handle + str(epilogue)) == data['users'][user]['handle_str'] for user in data['users'])):
                #userinfo[email] = {'passwd' : password, 'handle' : new_handle + str(epilogue), 'auth_user_id' : new_auth_user_id}
                data['users'][new_auth_user_id] = {
                    'u_id' : new_u_id, 
                    'name_first' : name_first, 
                    'name_last' : name_last, 
                    'email' : email,
                    'password' : password, 
                    'handle_str' : new_handle + str(epilogue),
                }
                return {'auth_user_id' : new_auth_user_id}
    else:   # unique handle, add straght away 
        #userinfo[email] = {'passwd' : password, 'handle' : new_handle, 'auth_user_id' : new_auth_user_id}
        data['users'][new_auth_user_id] = {
            'u_id' : new_u_id, 
            'name_first' : name_first, 
            'name_last' : name_last, 
            'email' : email,
            'password' : password,  
            'handle_str' : new_handle,
        }
        return {'auth_user_id' : new_auth_user_id}