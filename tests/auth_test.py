import pytest

from src.auth import auth
from src.error import InputError

def test_auth_email_format():
    assert auth_email_format('123@gmail@.com') == False, 'invalid email format'
    assert auth_email_format('jsfdsfds@ds123.con') == False, 'invalid email format'
    assert auth_email_format('myvalidemail@yahoogmail.com' == True, 'valid email format '

def test_auth_login_v1():
    assert auth_login_v1('adminemail@domain.com', '123456') == '999', 'login function broken'
    assert auth_login_v1('adminemail@domain.com', '123457') == None
