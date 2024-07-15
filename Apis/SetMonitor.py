import json

import requests

uid = input("access-token:")
class_id = input("class_id:")
user_id = input("user_id:")
headers = {
    "access-token": uid,
    "Content-Type": "application/json"
}
data = {"class_id": class_id, "user_id": user_id}
data_json = json.dumps(data)
resp = requests.post(url="http://127.0.0.1:5000/api/admin/change_role", headers=headers, data=data_json)
print(resp.json())
