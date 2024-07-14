from Apis.AppConfiguration import *


# 验证access-token装饰器
def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('access-token')
        if not token:
            return jsonify({'code': 403, 'message': 'Token is missing!'}), 403
        cursor.execute("SELECT * FROM admins WHERE access_token = %s", (token,))
        administrator = cursor.fetchone()
        if not administrator:
            return jsonify({'code': 403, 'message': 'Token is invalid!'}), 403
        return f(administrator, *args, **kwargs)

    return wrap


@app.route('/api/admin/create_class', methods=['POST'])
@token_required
def create_class(administrator):
    data = request.json
    class_name = data.get("class_name")
    cursor.execute(
        "INSERT INTO classes (class_name) VALUES (%s) RETURNING class_id",
        (class_name,)
    )
    class_id = cursor.fetchone()[0]
    database.commit()
    return jsonify({'class_id': class_id, 'message': 'Class created successfully'})


@app.route('/api/admin/generate_invite', methods=['POST'])
@token_required
def generate_invite(administrator):
    data = request.json
    class_id = data.get('class_id')
    invite_code = str(uuid.uuid4())[:8]  # 生成简短的邀请码
    expires_date = data.get('expires_date')

    cursor.execute("SELECT class_id FROM classes WHERE class_id = %s;", (class_id,))
    if not cursor.fetchone():
        return jsonify(
            {"code": 403,
             'message': 'Class not found or you do not have permission to generate invite for this class'}), 403

    cursor.execute(
        "INSERT INTO class_invites (class_id, invite_code, expires_date) VALUES (%s, %s, %s);",
        (class_id, invite_code, expires_date)
    )
    database.commit()
    return jsonify({"code": 200, 'invite_code': invite_code, 'message': 'Invite code generated successfully'})


@app.route('/api/admin/force_reg', methods=['POST'])
@token_required
def force_reg(administrator):
    data = request.json
    username = data.get("username")
    password = data.get("password")
    realname = data.get("realname")
    stu_id = data.get("stu_id")
    # email = data.get("email")
    access_token = str(uuid.uuid4())
    if username is None or password is None:
        return jsonify({'code': 403, 'message': 'Need username, password and email'}), 403

    cursor.execute("INSERT INTO users (stu_id, username, password, realname, access_token) VALUES (%s, %s, "
                   "%s, %s, %s) RETURNING user_id", (stu_id, username, password, realname, access_token))
    user_id = cursor.fetchone()[0]
    database.commit()
    return jsonify(
        {"code": 200, "message": "New user registered!", "user_id": user_id, "access_token": access_token}), 200


@app.route('/api/admin/force_del', methods=['POST'])
@token_required
def del_user(administrator):
    data = request.json
    user_id = data.get("user_id")
    cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    database.commit()
    return jsonify({"code": 200, "message": "User deleted!"}), 200


@app.route('/api/admin/change_role', methods=['POST'])
@token_required
def change_role(administrator):
    data = request.json
    user_id = data["user_id"]
    class_id = data["class_id"]
    role = data["role"]
    cursor.execute("SELECT role FROM class_users WHERE user_id = %s AND class_id = %s", (user_id, class_id))
    previous_role = cursor.fetchone()[0]
    cursor.execute("UPDATE class_users SET role = %s WHERE class_id = %s AND user_id = %s;", (role, class_id, user_id))
    cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
    username = cursor.fetchone()[0]
    database.commit()
    return jsonify(
        {"code": 200, "message": f"Successfully changed the role of {username} from {previous_role} to {role}"}), 200


@app.route('/api/admin/force_add', methods=['POST'])
@token_required
def force_add_class(administrator):
    data = request.json
    user_id = data["user_id"]
    class_id = data["class_id"]
    cursor.execute("INSERT INTO class_users (class_id, user_id) VALUES (%s, %s)", (class_id, user_id))
    database.commit()
    return jsonify({"code": 200, "message": f"Successfully added students into class {class_id}!"})
