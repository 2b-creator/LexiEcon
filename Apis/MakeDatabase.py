import json
from Apis.AppConfiguration import *
import hashlib
import uuid

cur = database.cursor()


def set_up_table():
    global cur
    # class
    cur.execute("""
        CREATE TABLE classes (
            class_id SERIAL PRIMARY KEY,
            class_name VARCHAR(100) NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    # user table
    cur.execute("""
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        stu_id INT NOT NULL UNIQUE,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(200) NOT NULL,
        realname VARCHAR(200) NOT NULL,
        email VARCHAR(100),
        access_token VARCHAR(200) NOT NULL UNIQUE,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE category (
        cate_id SERIAL PRIMARY KEY,
        cate_name VARCHAR(50) NOT NULL UNIQUE,
        cate_count INT NOT NULL
    );
    """)

    # class - users
    cur.execute("""
            CREATE TABLE class_users (
                class_user_id SERIAL PRIMARY KEY,
                class_id INT NOT NULL,
                user_id INT NOT NULL,
                role VARCHAR(50) DEFAULT 'member',
                FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """)

    # words table
    cur.execute("""
    CREATE TABLE words (
        word_id SERIAL PRIMARY KEY,
        word VARCHAR(100) NOT NULL,
        uk_phone VARCHAR(100) NOT NULL,
        us_phone VARCHAR(100) NOT NULL, 
        trans TEXT NOT NULL,
        cate_id INT NOT NULL,
        sentences TEXT NOT NULL,
        json_all JSON NOT NULL,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cate_id) REFERENCES category(cate_id) ON DELETE CASCADE
    );
    """)

    # task
    cur.execute("""
    CREATE TABLE tasks (
        task_id SERIAL PRIMARY KEY,
        task_name VARCHAR(100) NOT NULL,
        task_description VARCHAR(100),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # task - words
    cur.execute("""
    CREATE TABLE task_words (
        task_word_id SERIAL PRIMARY KEY,
        task_id INT NOT NULL,
        word_id INT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    );
    """)

    # user - tasks
    cur.execute("""
    CREATE TABLE user_tasks (
        user_task_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        task_id INT NOT NULL,
        class_id INT NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT '未开始',
        completion_date TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
        FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
    );""")

    # user - review
    cur.execute("""
    CREATE TABLE user_review_records (
        review_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        word_id INT NOT NULL,
        review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        review_result VARCHAR(50) NOT NULL,
        spell_correct_count INT NOT NULL DEFAULT 0,
        spell_wrong_count INT NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    );
    """)

    # admin
    cur.execute("""
        CREATE TABLE admins (
            admin_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            access_token VARCHAR(200) NOT NULL UNIQUE
        );
        """)

    # token
    cur.execute("""
    CREATE TABLE class_invites (
        invite_id SERIAL PRIMARY KEY,
        class_id INT NOT NULL,
        invite_code VARCHAR(50) NOT NULL UNIQUE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_date TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
    );
    """)

    new_uuid = uuid.uuid4()
    root_account = file.get("admin")
    name = root_account["username"]
    email = root_account["email"]
    password = root_account["password"]
    pwd_en = hashlib.md5()
    pwd_en.update(password.encode())
    pwd_en_hex = pwd_en.hexdigest()
    access_token = new_uuid

    cur.execute(f"""
    INSERT INTO admins (name, email, password, access_token) VALUES
    ('{name}', '{email}', '{pwd_en_hex}', '{access_token}');
    """)
    print("init success!")


def words_to_sql(filename: str):
    global cur
    with open(f"{filename}.json", "r", encoding="UTF-8") as fp:
        readlines = fp.readlines()
        cur.execute("INSERT INTO category (cate_name, cate_count) VALUES (%s, %s) RETURNING cate_id;",
                    (filename, len(readlines)))
        cate_id = cur.fetchone()[0]
        for line in readlines:
            read_lines_json = json.loads(line)
            word = read_lines_json["headWord"]
            uk_phone = read_lines_json["content"]["word"]["content"]["ukphone"]
            us_phone = read_lines_json["content"]["word"]["content"].get("usphone", "None")
            sentences = read_lines_json["content"]["word"]["content"].get("sentence", "None")
            if sentences != "None":
                sentences = sentences.get("sentences", "None")
            trans = str(read_lines_json["content"]["word"]["content"]["trans"])
            cur.execute(
                f"INSERT INTO words (word, uk_phone, us_phone, trans, cate_id, sentences, json_all) VALUES (%s, %s, "
                f"%s, %s, %s, %s, %s)",
                (word, uk_phone, us_phone, trans, cate_id, str(sentences), json.dumps(read_lines_json)))


if __name__ == "__main__":
    set_up_table()
    words_to_sql("../CET6")
    database.commit()
    cur.close()
    database.close()
