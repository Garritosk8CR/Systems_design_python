import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)
# Database configuration
server.config['MYSQL_HOST'] = 'localhost'
server.config['MYSQL_USER'] = 'root'
server.config['MYSQL_PASSWORD'] = 'admin'
server.config['MYSQL_DB'] = 'auth'
server.config['MYSQL_PORT'] = 3306

