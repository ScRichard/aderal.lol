from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import config
import database as db
import secrets

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)

# A helper function to add CORS headers manually
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allows all origins, modify this to specific domains if needed
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Route for handling CORS preflight requests (OPTIONS)
@app.route('/register', methods=['OPTIONS'])
def options():
    response = make_response()
    return add_cors_headers(response)

@app.route("/login", methods=['POST'])
def login():
    __password = request.form.get('password')

    __data = db.Handler()

    for user in __data.users:
        if bcrypt.check_password_hash(user['password'], config.get_salted_password(__password)):
            __data.update_access_cookie(user["username"])

            return jsonify(
                username=user["username"],
                access_token=user["access_cookie.token"]
            )

    return jsonify(Response="Invalid password")

@app.route("/register", methods=['POST'])
def register():
    print("Try")
    __username = request.form.get('username')
    __token = request.form.get('token')

    print(__username, __token)

    __data = db.Handler()

    if not __data.is_username_valid(__username):
        return jsonify(Response="Invalid name")

    if __data.is_token_used_and_update(__token):
        return jsonify(Response="Invalid token")

    __not_hashed_password = secrets.token_hex(18)

    __salted_and_hashed = bcrypt.generate_password_hash(config.get_salted_password(__not_hashed_password)).decode('utf-8')

    __data.add_user(__username, __salted_and_hashed)

    return jsonify(
        Response="Registration successful",
        Password=__not_hashed_password
                   )



if __name__ == "__main__":
    app.run(debug=True)