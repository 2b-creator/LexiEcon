# LexiEcon 使用手册

## 简单流程

欢迎使用 LexiEcon，下面是使用这个项目的一系列流程。

## 部署后端

### 拉取源码安装依赖

后端地址：[2b-creator/LexiEcon (github.com)](https://github.com/2b-creator/LexiEcon)，你可以直接阅读后端的 Readme 更加详细一些。

这里以 Ubuntu 系统为例，第一步为安装 git 拉取源代码并安装 pip 包：

```sh
sudo apt update
sudo apt install git
sudo git clone https://github.com/2b-creator/LexiEcon.git
sudo apt install python3-pip
cd LexiEcon/
pip install -r requirements.txt
```

等待安装完毕。

### 安装 PostgreSQL

运行命令安装：

```sh
sudo apt update
sudo apt install postgresql
```

刚安装好 PostgreSQL 时会自动新创建一个数据库用户和一个 Linux 系统用户，用户名都是 postgres，用以作为超级管理员管理数据库。

下面建议更改 postgres 的数据库用户与系统用户密码。

```sh
sudo -u postgres psql
```

然后命令行前面的提示符会变成 `postgres=#`。接下来通过以下将数据库用户 postgres 的密码更改为 `your_password`。

```sql
ALTER USER postgres WITH PASSWORD 'your_password';
```

记得结尾加`;` 代表数据库命令结束，如果忘记了前面的提示符会变成 `postgres-#`。所以记得加上 `;`。

然后使用 `\q` 退出数据库，接着使用以下命令修改 Linux 系统用户 postgres 的密码。

```sh
sudo passwd -d postgres 
sudo -u postgres passwd
```

### 创建数据库以及指定用户

为了安全起见，建议创建一个用户并管理该数据库，执行以下命令创建数据库用户 `lexi_econ`：

```sh
sudo -u postgres createuser --pwprompt lexi_econ
```

其中 `--pwprompt` 表示建立该用户时设置密码，然后进入数据库

```sh
sudo -u postgres psql
```

创建数据库 `lexi_econ_db`

```sql
CREATE DATABASE lexi_econ_db OWNER lexi_econ;
```

创建完毕后进入刚刚 clone 的项目，编辑 `config.toml`， 在表 `[admin]` 中指定填写 lexi_econ 超级管理员的登录账号和密码以便操作 AdminApi，`[book]` 则填写词库的名称，有关词库我们可以前往 https://github.com/kajweb/dict.

```toml
# database set up
[database]
host = "127.0.0.1"
port = "5432"
name = "lexi_econ_db"
user = "lexi_econ"
password = "your_password"

# root user config and init
[admin]
username = "lexi_root"
password = "lexi_root_password"
email = "root@example.com"

[book]
name = ["CET4luan_1"]
```

在开始使用之前，请确保你的 Config.toml 配置正确，并运行MakeDatabase.py 直到控制台显示 init Success 表示初始化完成。

```sh
python ./MakeDatabase.py
```

最后运行

```sh
python ./main.py
```

该服务默认的端口是 5000，可根据实际情况进行更改。

## 获取教师 access-token

使用 `POST` 方法请求 `/api/client/login/admin` 端点获取 access-token。

```python
import hashlib
import json

import requests
from Apis.AppConfiguration import *

headers = {
    "Content-Type": "application/json"
}

root_account = file.get("admin")  # file = toml.load("./config.toml")

# 加密验证密码
password = root_account["password"]
pwd_en = hashlib.md5()
pwd_en.update(password.encode())
pwd_en_hex = pwd_en.hexdigest()

data = {"username": root_account["username"], "password": root_account["password"]}
data_json = json.dumps(data)
resp = requests.post(url="http://127.0.0.1:5000/api/client/login/admin", headers=headers, data=data_json)
access_token = resp.json()["access_token"]
print(access_token)
```

## 导入学生

你需要准备一个电子表必须包含学号，班级，姓名列，数据结构类似于这样

| 学号       | 姓名   | 性别 | 民族 | 政治面貌 | 生源地 | 所在院系名称 | 校内专业名称 | 班级    | 年级 | 入学年份 | 学制 |
| ---------- | ------ | ---- | ---- | -------- | ------ | ------------ | :----------- | ------- | ---- | -------- | ---- |
| 2023243101 | 陈薪宇 | 男   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243102 | 陈宇衡 | 女   | 汉族 | 共青团员 | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243103 | 储承栖 | 女   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243104 | 付雪晴 | 女   | 汉族 | 共青团员 | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243105 | 葛翔   | 男   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243106 | 葛雨璇 | 女   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243107 | 管海洋 | 男   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243109 | 梁萍   | 女   | 汉族 | 共青团员 | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |
| 2023243110 | 陆振阳 | 男   | 汉族 | 群众     | 江苏省 | 经济学院     | 经济统计学   | 23经统1 | 2023 | 2023     | 4    |

将其重命名为 ids.xlsx 放入服务端的 Apis 文件夹中然后运行 `python ./ImportStudents.py` 即可，然后按照提示输入 `access-token` 最后输出 `out.xlsx` 文件包含学生的初始密码与 user_id 以及各个班级对应的 class_id

下面是输出的样例:

- 表一

| user_id | 学号       | 姓名   | 班级 | 初始密码 |
| ------- | ---------- | ------ | ---- | -------- |
| 1       | 2022326128 | 陈思嘉 | 4    | CAc1kI7J |
| 2       | 2023241101 | 陈曦   | 4    | SQQvAz4b |
| 3       | 2023241102 | 戴安妮 | 4    | peRILFTR |
| 4       | 2023241103 | 顾瑞   | 4    | u4biqObt |
| 5       | 2023241104 | 郭清婷 | 4    | lS7Oc0OG |
| 6       | 2023241105 | 黄湘怡 | 4    | G0J2e80b |
| 7       | 2023241106 | 吉玉馨 | 4    | GlzjdR7U |

- 表二

| 23经统1 | 23经统2 | 23金融2 | 23国贸1 | 23金融1 | 23国贸2 | 23电商 |
| ------- | ------- | ------- | ------- | ------- | ------- | ------ |
| 1       | 2       | 3       | 4       | 5       | 6       | 7      |

## 设置班长

班级里的班长可以负责任务的发布，使用 `/api/admin/change_role` 端点更改学生角色，默认为 `member` 下面我将举例来设置班长，例如将 `23国贸1` 的陈思嘉设置为他们班的班长

> SetMonitor.py

```python
import json

import requests

uid = input("access-token:")
class_id = input("class_id:")
user_id = input("user_id:")
headers = {
    "access-token": uid,
    "Content-Type": "application/json"
}
data = {"class_id": class_id, "user_id": user_id}
data_json = json.dumps(data)
resp = requests.post(url="http://127.0.0.1:5000/api/admin/change_role", headers=headers, data=data_json)
print(resp.json())
```

在运行这段代码的时候，根据提示输入 `user_id` 与 `class_id` 即可。

## 数据库维护

可以使用pgadmin v4
