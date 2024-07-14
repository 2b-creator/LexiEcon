# LexiEcon api

## Introduction
This is a LexiEcon api document.

## Set up postgreSQL
In this project, I chose to use PostgreSQL as the storage database engine. The version tested on my machine is v12.

## Config.toml

Config.toml is the configuration file, you need to make some minor modifications.

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
username = "root"
password = "root_password"
email = "root@example.com"

[book]
name = ["CET4luan_1"]
```

In the [database] table, fill in the host user and password of your database. In psql, "5432" is the default port.

In the [admin] field, fill in the API's super administrator account. This account can use any API at will.

In the table [book], fill in the textbooks for the words you want to memorize. Here I take a CET4luan_1.json file I uploaded as an example. All databases can be sourced from here: https://github.com/kajweb/dict.

## Prepare database

Before you start using it, make sure your Config.toml is configured correctly and run MakeDatabase.py until the console displays `init Success` to indicate that initialization is complete.

```sh
python ./MakeDatabase.py
```

and

```sh
python ./main.py
```

## Clone words repository
```shell
git clone https://github.com/kajweb/dict.git
```

