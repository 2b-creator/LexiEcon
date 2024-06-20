import hashlib
import json

import requests


def teacher_test():
    uid = "7158792e-0dbc-4f60-8ad7-40a5971c3dff"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }

    data = {
        "user_id": 1,
        "class_id": 1,
        "role": "monitor"
    }

    data_json = json.dumps(data)

    resp = requests.post(url="http://127.0.0.1:5000/api/admin/change_role", headers=headers, data=data_json)
    print(resp.json())


def stu_test():
    uid = "eeb834ca-6694-41a6-9db7-512aaff33d61"

    headers = {
        "access-token": uid,
        "Content-Type": "application/json"
    }

    data = {
        "class_id": 1,
        "task_id": 1,
    }

    data_json = json.dumps(data)

    resp = requests.get(url="http://127.0.0.1:5000/api/users/task/check", headers=headers)
    print(resp.json())

stu_test()
