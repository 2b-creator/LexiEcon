import json

import numpy as np
import pandas as pd
import hashlib
import base64
import secrets
import string

import requests

uid = "9ccc3f05-5930-4f2b-a5ee-3346364eb84e"

headers = {
    "access-token": uid,
    "Content-Type": "application/json"
}


def generate_password(length=8):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def apply_hash(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    hashed_bytes = md5.digest()
    res = base64.b64encode(hashed_bytes).decode('utf-8')
    return res


sheet = pd.read_excel("./ids.xlsx")
rec = []
rec_2 = []
passwd_rec = []
user_id_ls = []
stu_id = list(sheet["学号"][1:])
realname = list(sheet["姓名"][1:])
class_name = list(sheet["班级"][1:])
class_set = set(class_name)
class_dic ={}

for i in range(len(stu_id)):
    password = generate_password()
    passwd_rec.append(password)
    rec.append([stu_id[i], realname[i], class_name[i], password])

for i in iter(class_set):
    data_2 = {"class_name": i}
    data_json = json.dumps(data_2)
    resp = requests.post(url="http://127.0.0.1:5000/api/admin/create_class", headers=headers, data=data_json)
    class_id = resp.json()["class_id"]
    class_dic[i] = class_id

df1 = pd.DataFrame(rec, columns=["学号", "姓名", "班级", "初始密码"])
df1.to_excel("./out.xlsx")

for i in range(len(stu_id)):
    rec_2.append([stu_id[i], realname[i], class_dic[class_name[i]], passwd_rec[i]])
    dic = {"stu_id": stu_id[i], "username": stu_id[i], "realname": realname[i], "password": apply_hash(passwd_rec[i])}
    data_json = json.dumps(dic)
    resp = requests.post(url="http://127.0.0.1:5000/api/admin/force_reg", headers=headers, data=data_json)
    user_id_ls.append(resp.json()["user_id"])

for i in range(len(user_id_ls)):
    dic = {"user_id": user_id_ls[i], "class_id": class_dic[class_name[i]]}
    data_json = json.dumps(dic)
    resp = requests.post(url="http://127.0.0.1:5000/api/admin/force_add", headers=headers, data=data_json)
print(df1)
