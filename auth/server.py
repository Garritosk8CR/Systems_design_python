import jwt, datetime, os # type: ignore
from flask import Flask, request # type: ignore
from flask_mysqldb import MySQL
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
server = Flask(__name__)
mysql = MySQL(server)
# Database configuration
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')
server.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))  # Convert to int


@server.route('/login', methods=['POST'])
def login():
    logging.info("login called")
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return 'Missing credentials', 401

    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT * FROM users WHERE email=%s", (auth.username,)
    )
    if result > 0:
        user = cursor.fetchone()
        email = user[1]
        password = user[2] 
        if auth.username != email or auth.password != password:
            return 'Invalid credentials (password or email)', 401
        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True), 200
    else:
        return 'Invalid credentials or user does not exist', 401
    
@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return 'Missing credentials', 401
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get('JWT_SECRET'), algorithms=['HS256'])
    except:
        return 'Not authorized', 403

    return decoded, 200
def createJWT(username, secret, authz):
    payload = {
        'username': username,
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        'admin': authz
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)