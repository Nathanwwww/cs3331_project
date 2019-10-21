import sqlite3
from server import app
from flask import Flask, request, json, jsonify,render_template
from flask_restplus import Resource, Api
from src.user import User
from flask_cors import CORS

@app.route('/hello')
def hello():
    return 'hello'

#implement the login function, frontend send the data to here and pass to backend function


@app.route('/login', methods=['POST']) 
def login():
    inputJSON = request.get_json()
    username = inputJSON['username']
    password = inputJSON['password']
    if User.login(username,password):
        return jsonify(status=200),200
    else:
        return jsonify(status=401),401

# implement the register function, frontend send the data to here and pass to backend function
@app.route("/register", methods=['POST']) 
def register():
    inputJSON = request.get_json()
    username = inputJSON['username']
    password = inputJSON['password']
    email = inputJSON['email']
    result = User.createUser(username, password,email)

    if result:
        return jsonify(status = 200),200
    else:
        return jsonify(status=401),401

# implement the reset function, frontend send the data to here and pass to backend function
@app.route("/reset", methods=['POST']) 
def reset():
    inputJSON = request.get_json()
    password = inputJSON['password']
    username = inputJSON['username']
    print(password, len(password), type(password))
    result = User.reset(password,username)

    if result:
        return jsonify(status = 200)
    else:
        return jsonify(status = 401)

