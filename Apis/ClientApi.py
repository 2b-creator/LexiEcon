import requests
from flask import send_from_directory

from Apis.AppConfiguration import *


@app.route('/api/client/login/user', methods=['POST'])
def login_users():
    data = request.json
    username = data["username"]
    password = data["password"]
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    remote_pwd = cursor.fetchone()[0]
    if password == remote_pwd:
        cursor.execute("SELECT access_token FROM users WHERE username=%s", (username,))
        token = cursor.fetchone()[0]
        return jsonify({"code": 200, "access_token": token, "message": "Login success"}), 200
    return jsonify({"code": 403, "message": "Sorry, Authentication failure, try again."}), 403


@app.route('/api/client/login/admin', methods=['POST'])
def login_admin():
    data = request.json
    username = data["username"]
    password = data["password"]
    cursor.execute("SELECT password FROM admins WHERE name=%s", (username,))
    remote_pwd = cursor.fetchone()[0]
    if password == remote_pwd:
        cursor.execute("SELECT access_token FROM admins WHERE name=%s", (username,))
        token = cursor.fetchone()[0]
        return jsonify({"code": 200, "access_token": token, "message": "Login success"}), 200
    return jsonify({"code": 403, "message": "Sorry, Authentication failure, try again."}), 403


@app.route('/api/client/get_cate', methods=['GET'])
def check_cate():
    cursor.execute("SELECT cate_id, cate_name, cate_count FROM public.category")
    getdata = cursor.fetchall()
    ls = []
    for i in getdata:
        dic = {"cate_id": int(i[0]), "cate_name": i[1]}
        ls.append(dic)
    return jsonify({"data": ls, "code": 200}), 200


@app.route('/api/client/latest', methods=['GET'])
def check_version():
    latest_version = "1.0.0.1"
    return jsonify({"data": latest_version, "code": 200}), 200


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('../', filename, as_attachment=True)


@app.route('/api/client/query', methods=['GET'])
def get_info():
    access_token = request.args.get("access_token")
    cursor.execute("SELECT realname FROM users WHERE access_token=%s", (access_token,))
    realname = cursor.fetchone()[0]
    return jsonify({"code:": 200, "realname": realname}), 200
