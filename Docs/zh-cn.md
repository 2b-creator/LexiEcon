# LexiEcon 使用手册

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

