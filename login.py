import os
from passlib.apache import HtpasswdFile
import json

# function for adding User
def add_user(username,password):
    cwd = os.path.abspath(__file__)[:-8]
    if os.path.exists(cwd+".htpasswd") == False:
        ht = HtpasswdFile(cwd+".htpasswd", new=True)
        result = ht.set_password(username, password)
        ht.save()
        return result
    else:
        ht = HtpasswdFile(cwd+".htpasswd")
        result = ht.set_password(username, password)
        ht.save()
        if result == False:
            return True
        else:
            return False

# check username and password 
def check_user_password_htpasswd(username,password):
    cwd = os.path.abspath(__file__)[:-8]
    ht = HtpasswdFile(cwd+".htpasswd")
    return ht.check_password(username, password)

def login(data):
    data_dict = json.loads(data)
    username = data_dict["username"]
    password = data_dict["password"]
    if check_user_password_htpasswd(username,password):
        return "True"
    else:
        return "invalid password"

