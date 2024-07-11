import hashlib
import json

import requests


def teacher_test():
    uid = "e007b9c9-516c-44f3-9ce9-728319dc1889"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }
    data = {"username": "lexier", "password": "liAS0JuBcNkS8GafbX2dBw==", "stu_id": 191981001, "email": "test111@test.com"}

    data_2 = {"class_id": 1, "user_id": 1, "role": "monitor"}
    data_json = json.dumps(data)

    resp = requests.post(url="http://127.0.0.1:5000/api/admin/force_reg", headers=headers, data=data_json)
    print(resp.json())


def stu_test():
    uid = "806e5a8d-23f9-4f31-96bc-dacf89cbfe79"
    # uid = "f607ea89-5371-4b4b-aecf-423933cd0bde"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }

    data = {
        "task_id": 1,
        "class_id":1
    }
    data_2 = {"invite_code": "79187fd2"}
    data_json = json.dumps(data)

    resp = requests.post(url="http://127.0.0.1:5000/api/users/task/release", headers=headers, data=data_json)
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
