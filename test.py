import hashlib
import json

import requests


def teacher_test():
    uid = "e007b9c9-516c-44f3-9ce9-728319dc1889"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }
    data = {"username": "lexi", "password": "CY9rzUYh03PK3k6DJie09g==", "stu_id": 19198100, "email": "test@test.com"}

    data_2 = {"class_id": 1, "user_id": 1, "role": "monitor"}
    data_json = json.dumps(data_2)

    resp = requests.post(url="http://127.0.0.1:5000/api/admin/change_role", headers=headers, data=data_json)
    print(resp.json())


def stu_test():
    uid = "806e5a8d-23f9-4f31-96bc-dacf89cbfe79"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }

    data = {
        "task_id": 1
    }
    data_2 = {"invite_code": "79187fd2"}
    data_json = json.dumps(data)

    resp = requests.post(url="http://127.0.0.1:5000/api/users/task/finish", headers=headers, data=data_json)
    print(resp.json())


# 717a92e0-dd92-444a-a461-3536ebba6095

def client_test():
    uid = "eeb834ca-6694-41a6-9db7-512aaff33d61"

    headers = {
        # "access-token": uid,
        "Content-Type": "application/json"
    }

    data = {
        "username": "root",
        "password": "a9bb01fe0dd1141d97407db3610cc336",
    }

    data_json = json.dumps(data)

    resp = requests.post(url="http://127.0.0.1:5000/api/client/login/admin", data=data_json, headers=headers)
    print(resp.status_code)
    print(resp.json())


stu_test()
