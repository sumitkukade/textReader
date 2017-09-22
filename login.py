import os
from passlib.apache import HtpasswdFile
import json
def add_user(username,password):
    cwd = os.path.abspath(__file__)[:-8]
    if os.path.exists(".htpasswd") == False:
        ht = HtpasswdFile(".htpasswd", new=True)
        result = ht.set_password(username, password)
        ht.save()
	return result
    else:
        ht = HtpasswdFile(".htpasswd")
        result = ht.set_password(username, password)
        ht.save()
        if result == False:
            return True

def check_user_password_htpasswd(username,password):
    ht = HtpasswdFile(".htpasswd")
    return ht.check_password(username, password)

def login(data):
    data_dict = json.loads(data)
    username = data_dict["username"]
    password = data_dict["password"]
    if check_user_password_htpasswd(username,password):
        return "True"
    else:
        return "invalid password"

