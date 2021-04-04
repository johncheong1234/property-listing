from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import dbconnector

import random
import string

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    jsonData = request.get_json()
    print(jsonData)
    
    if "username" in jsonData and "password" in jsonData:
        username = jsonData["username"]
        password = jsonData["password"]
        query = "SELECT * FROM User WHERE username = %s AND password = %s;"
        params = (username, password)
        
        user = dbconnector.select_one_params(query, params)
        if user != None:
            userId = user["userId"]
            apiKey = generateApiKey(userId)
            if apiKey != None:
                return jsonify({
                    "code": 200,
                    "data": {
                        "userId": userId,
                        "apiKey": apiKey
                    }
                })
            return jsonify({
                "code": 500,
                "message": "Error: Unable to create API Key."
            })
        return jsonify({
            "code": 401,
            "message": "Please enter a valid login and password"
        })
    return jsonify({
        "code": 400,
        "message": "Incorrect parameters."
    })

@app.route('/apilogin', methods=['POST'])
def apilogin():
    jsonData = request.get_json()
    print(jsonData)
    
    if "userId" in jsonData and "apiKey" in jsonData:
        userId = jsonData["userId"]
        apiKey = jsonData["apiKey"]

        query = "SELECT * FROM User WHERE userId = %s AND apiKey = %s;"
        params = (userId, apiKey)

        user = dbconnector.select_one_params(query, params)
        if user != None:
            return jsonify({
                "code": 200,
                "data": user
            })
        return jsonify({
            "code": 401,
            "message": "Invalid API Key."
        }, 401)
    return jsonify({
        "code": 400,
        "message": "Incorrect parameters."
    }, 400)

@app.route('/create', methods=['POST'])
def create():
    jsonData = request.get_json()
    print(jsonData)
    
    if "username" in jsonData and "password" in jsonData:
        query = "INSERT INTO User(username, name, password, email, nric) VALUE(%s, %s, %s, %s, %s);"
        params = (jsonData["username"], jsonData["name"], jsonData["password"], jsonData["email"], jsonData["nric"])
        
        id = dbconnector.insert_parameters(query, params)
        print(f"Inserted {id}")
        if id != None:
            return jsonify(
                {
                    "code": 200,
                    "data": id
                }
            ), 200
        return jsonify(
            {
                "code": 500,
                "message": "Unable to insert."
            }
        ), 500
    return jsonify({
        "code": 400,
        "message": "Incorrect parameters."
    }, 400)

def generateApiKey(userId):
    apiKey = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    
    query = "UPDATE User SET apiKey = %s WHERE userId = %s"
    params = (userId, apiKey)
    dbconnector.execute_parameters(query, params)

    return apiKey

@app.route('/getuser/<string:userid>', methods=['POST','GET'])
def getuser(userid):
    query = "SELECT * FROM User WHERE userId = %s"
    params = (userid,)

    user = dbconnector.select_one_params(query, params)
    return user

if __name__ == '__main__':
    app.run(port=8001, debug=True)
