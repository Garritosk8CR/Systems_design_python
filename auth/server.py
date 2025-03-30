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

server.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return 'Missing credentials', 401

    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT * FROM users WHERE email=%s", (auth.username,)
    )
    if result > 0:
        user = cursor.fetchone()
        email = user[0]
        password = user[1]

        if auth.username != email or auth.password != password:
            return 'Invalid credentials', 401
        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True), 200

    else:
        return 'Invalid credentials', 401