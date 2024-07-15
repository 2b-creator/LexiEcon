import hashlib
import json

import requests
from Apis.AppConfiguration import *

headers = {
    "Content-Type": "application/json"
}

root_account = file.get("admin")  # file = toml.load("./config.toml")
password = root_account["password"]
pwd_en = hashlib.md5()
pwd_en.update(password.encode())
pwd_en_hex = pwd_en.hexdigest()
data = {"username": root_account["username"], "password": pwd_en_hex}
data_json = json.dumps(data)
resp = requests.post(url="http://127.0.0.1:5000/api/client/login/admin", headers=headers, data=data_json)
access_token = resp.json()["access_token"]
print(access_token)
