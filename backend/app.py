import os
import secrets

from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt

import config
import database as db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)

@app.after_request
def add_headers(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return response

@app.route("/login", methods=['POST'])
def login():
    __password = request.json['password']

    __data = db.Handler()

    for user in __data.users:
        if bcrypt.check_password_hash(user['password'], config.get_salted_password(__password)):
            __data.update_access_cookie(user["username"])

            return jsonify(
                username=user["username"],
                access_token=user["access_cookie.token"]
            )

    return jsonify(Response="Invalid password")

@app.route("/register", methods=['GET','POST'])
def register():
    __username = request.json['username']
    __token = request.json['token']

    print(__token)

    __data = db.Handler()

    if not __data.is_username_valid(__username):
        print("returned invalid name")
        return jsonify(
            Type="Error",
            Response="Invalid name"
        )

    if __data.is_token_used_and_update(__username, __token):
        print("returned invalid token")
        return jsonify(
            Type="Error",
            Response="Invalid token"
        )

    __not_hashed_password = secrets.token_hex(18)

    __salted_and_hashed = bcrypt.generate_password_hash(
        config.get_salted_password(__not_hashed_password)).decode('utf-8')

    __data.add_user(__username, __salted_and_hashed)
    print("returned registration success")
    return jsonify(
        Type="Success",
        Response=__not_hashed_password
                   )



if __name__ == "__main__":
    app.run(debug=True)