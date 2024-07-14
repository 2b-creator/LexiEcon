from flask import Flask, request, jsonify
import psycopg2
import toml
import uuid
from functools import wraps

try:
    file = toml.load("Apis/config.toml")
except FileNotFoundError:
    file = toml.load("./config.toml")
config = file.get("database")
host = config.get("host")
db = config.get("name")
port = config.get("port")
user = config.get("user")
pwd = config.get("password")

app = Flask(__name__)

database = psycopg2.connect(database=db, user=user, password=pwd, host=host, port=port)
cursor = database.cursor()
