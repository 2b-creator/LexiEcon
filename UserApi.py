from AppConfiguration import *


def auth_monitor(users, class_id):
    # 鉴权是否为 monitor
    cursor.execute("SELECT role FROM class_users WHERE user_id = %s AND class_id = %s;", (users[0], class_id))
    get_role = cursor.fetchone()[0]
    return get_role


def token_required_users(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('access-token')
        if not token:
            return jsonify({'code': 403, 'message': 'Token is missing!'}), 403
        cursor.execute("SELECT * FROM users WHERE access_token = %s", (token,))
        teacher = cursor.fetchone()
        if not teacher:
            return jsonify({'code': 403, 'message': 'Token is invalid!'}), 403
        return f(teacher, *args, **kwargs)

    return wrap


@app.route('/api/users/join', methods=['POST'])
@token_required_users
def join_class(users):
    data = request.json
    post_invite_code = data["invite_code"]
    cursor.execute("SELECT class_id FROM class_invites WHERE invite_code=%s;", (post_invite_code,))
    class_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO class_users (class_id, user_id) VALUES (%s, %s)", (class_id, users[0]))
    cursor.execute("SELECT class_name FROM classes WHERE class_id=%s", (class_id,))
    class_name = cursor.fetchone()[0]
    database.commit()
    return jsonify({"code": 200, "message": f"Successfully joined class '{class_name}'"}), 200


@app.route('/api/users/task/new', methods=['POST'])
@token_required_users
def release_new_task(users):
    data = request.json
    class_id = data["class_id"]
    if auth_monitor(users, class_id) != "monitor":
        return jsonify({"code": 403,
                        "message": f"There is no permission for "
                                   f"role {auth_monitor(users, class_id)[1]} in class {class_id}"}), 403

    task_name = data["name"]
    cursor.execute("SELECT task_id FROM tasks WHERE task_name = %s", (task_name,))
    if cursor.fetchone():
        return jsonify({"code": 403, "message": "A same task_name was created before."}), 403

    cursor.execute("INSERT INTO tasks (task_name) VALUES (%s) RETURNING task_id", (task_name,))
    task_id = cursor.fetchone()[0]
    database.commit()
    return jsonify({"code": 200, "task_id": task_id, "message": f"Task {task_name} was successfully created"}), 200


@app.route('/api/users/task/assign', methods=['POST'])
@token_required_users
def assign_task(users):
    total = 0
    data = request.json
    class_id = data["class_id"]
    if auth_monitor(users, class_id) != "monitor":
        return jsonify({"code": 403,
                        "message": f"There is no permission for "
                                   f"role {auth_monitor(users, class_id)[1]} in class {class_id}"}), 403

    task_id = data["task_id"]
    words = list(data["words"])
    for i in words:
        i = dict(i)
        cate_id = i["cate_id"]
        start = int(i["start"])
        end = int(i["end"])
        total += (end - start + 1)
        cursor.execute("SELECT word_id FROM words WHERE cate_id = %s ORDER BY word_id OFFSET %s LIMIT %s;",
                       (cate_id, start - 1, end - start + 1))
        res = cursor.fetchall()
        for row in res:
            cursor.execute("INSERT INTO task_words (task_id, word_id) VALUES (%s, %s)", (task_id, row[0]))
    database.commit()
    return jsonify({"code": 200, "message": f"{total} words was assigned to task_id:{task_id}"})


@app.route('/api/users/task/release', methods=['POST'])
@token_required_users
def release_task(users):
    data = request.json
    class_id = int(data["class_id"])
    task_id = int(data["task_id"])
    assign_stu = data.get("assign_stu_id", "all")
    if auth_monitor(users, class_id) != "monitor":
        return jsonify({"code": 403,
                        "message": f"There is no permission for "
                                   f"role {auth_monitor(users, class_id)[1]} in class {class_id}"}), 403
    if assign_stu == "all":
        cursor.execute("SELECT user_id FROM class_users WHERE class_id = %s", (class_id,))
        user_id_collection = cursor.fetchall()
        for i in user_id_collection:
            cursor.execute("INSERT INTO user_tasks (user_id, task_id, class_id, status) VALUES (%s, %s, %s, %s)",
                           (i[0], task_id, class_id, "未开始"))
    else:
        user_id_ls = list(assign_stu)
        for i in user_id_ls:
            cursor.execute("INSERT INTO user_tasks (user_id, task_id, class_id, status) VALUES (%s, %s, %s, %s)",
                           (i, task_id, class_id, "未开始"))
    database.commit()
    return jsonify({"code": 200, "message": f"Task {task_id} was successfully assigned to {class_id}"})


@app.route('/api/users/task/query', methods=['GET'])
# @token_required_users
def query_tasks():
    name = request.args.get("task_name")
    if name is not None:
        cursor.execute("SELECT task_id FROM tasks WHERE task_name = %s", (name,))
        task_id = cursor.fetchone()[0]
        return jsonify({"task_id": task_id})
    else:
        cursor.execute("SELECT task_id,task_name FROM tasks;")
        all_id = cursor.fetchall()
        ls = []
        for i in all_id:
            dic = {"task_id": i[0], "task_name": i[1]}
            ls.append(dic)
        return jsonify({"data": ls, "code": 200}), 200


@app.route('/api/users/task/check', methods=['GET'])
@token_required_users
def check_tasks(users):
    user_id = users[0]
    cursor.execute("SELECT task_id, class_id, status FROM user_tasks WHERE user_id = %s", (user_id,))
    all_tasks = cursor.fetchall()
    ls = []
    for i in all_tasks:
        dic = {"task_id": i[0], "class_id": i[1], "status": i[2]}
        ls.append(dic)
    return jsonify({"data": ls, "code": 200}), 200


@app.route('/api/users/class/info', methods=['GET'])
@token_required_users
def class_users(users):
    args = set(request.args.items())
    cursor.execute("SELECT class_id, user_id, role FROM class_users WHERE user_id = %s", (users[0],))
    res = cursor.fetchall()
    ls = []
    for i in res:
        dic = {"class_id": i[0], "user_id": i[1], "role": i[2]}
        set_dic = set(dic.items())
        if args is not None:
            if args.issubset(set_dic):
                ls.append(dic)
        else:
            ls.append(dic)
    all_dic = {"data": ls, "code": 200}
    return jsonify(all_dic), 200


@app.route('/api/users/words/submit', methods=['POST'])
@token_required_users
def task_submit_condition(users):
    user_id = users[0]
    data = request.json
    word_id = int(data["word_id"])
    test_cate = data["review_category"]
    situation = data["situation"]
    if test_cate == "spell":
        if situation == "true":
            cursor.execute("SELECT spell_correct_count FROM user_review_records WHERE user_id = %s AND word_id = %s",
                           (user_id, word_id))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO user_review_records (user_id, word_id) VALUES (%s, %s)", (user_id, word_id))
            cursor.execute("SELECT spell_correct_count FROM user_review_records WHERE user_id = %s AND word_id = %s",
                           (user_id, word_id))
            count = int(cursor.fetchone()[0])
            count += 1
            cursor.execute(
                "UPDATE user_review_records SET spell_correct_count = %s WHERE user_id = %s AND word_id = %s",
                (count, user_id, word_id))
        elif situation == "false":
            cursor.execute("SELECT spell_wrong_count FROM user_review_records WHERE user_id = %s AND word_id = %s",
                           (user_id, word_id))
            count = int(cursor.fetchone()[0])
            count += 1
            cursor.execute(
                "UPDATE user_review_records SET spell_wrong_count = %s WHERE user_id = %s AND word_id = %s",
                (count, user_id, word_id))
        else:
            return jsonify({"code": 405, "message": "Bad situation, must be 'false' or 'true'! "}), 405


@app.route('/api/users/task/finish', methods=['POST'])
@token_required_users
def finish_task(users):
    data = request.json
    user_id = users[0]
    task_id = data["task_id"]
    cursor.execute("UPDATE user_tasks SET status = %s WHERE user_id = %s AND task_id = %s",
                   ("已完成", user_id, task_id))
    dic = {"code": 200, "message": f"Task {task_id} is finished."}
    return jsonify(dic), 200
