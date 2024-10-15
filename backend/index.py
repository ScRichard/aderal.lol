from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def register():
    return

@app.route("/register", methods=['POST'])
def login():
    return

if __name__ == "__main__":
    app.run(debug=True)