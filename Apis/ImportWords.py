from Apis.AppConfiguration import *
import json

cur = database.cursor()


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
    words_to_sql("../CET6.json")