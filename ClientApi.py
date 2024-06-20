import requests
import RSAEncryptPasswords

from AppConfiguration import *


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
    cursor.execute("SELECT password FROM admin WHERE username=%s", (username,))
    remote_pwd = cursor.fetchone()[0]
    if password == remote_pwd:
        cursor.execute("SELECT access_token FROM users WHERE username=%s", (username,))
        token = cursor.fetchone()[0]
        return jsonify({"code": 200, "access_token": token, "message": "Login success"}), 200
    return jsonify({"code": 403, "message": "Sorry, Authentication failure, try again."}), 403
