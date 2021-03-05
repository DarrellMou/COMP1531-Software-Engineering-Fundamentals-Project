import pytest

from src.error import InputError
from src.auth import auth_login_v1, auth_email_format, auth_register_v1

def test_auth_email_format():
    assert auth_email_format('123@gmailcom') == False, 'invalid email format'
    assert auth_email_format('jsfdsfdsds123.con') == False, 'invalid email format'
    assert auth_email_format('myvalidemail@yahoogmail.com') == True, 'valid email format'

def test_auth_login_v1():
    assert auth_login_v1('example1@hotmail.com', 'password1') == {'auth_user_id' : 35746842521}, 'login function broken'
    with pytest.raises(InputError):
    	auth_login_v1('123456789@@gmail.com', '123456') # invalid email format 
    	auth_login_v1('adminemail@domain.com', '123456off')	# valid format but password doesn't match
        
def test_auth_register_v1():
    with pytest.raises(InputError):
        auth_register_v1('sampleemail1gmail.com', 'password1', 'test', 'user1')
        auth_register_v1('sampleemail1@gmail.com', 'password1', 'test', 'user1')
        auth_register_v1('sampleemail2@gmail.com', 'passwo', 'test', 'user1')
        auth_register_v1('sampleemail2@gmail.com', 'passwo', '', 'user1')