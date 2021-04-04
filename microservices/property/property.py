from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import dbconnector

import numbers

app = Flask(__name__)
CORS(app)

@app.route("/property", methods=["POST"])
def get():
    jsonData = request.get_json()
    print(jsonData)
    if(jsonData["propertyId"] != None):
        p = dbconnector.select_one_parameters("SELECT * FROM Property WHERE propertyId = %s", (jsonData["propertyId"],))
        return jsonify({
                "code": 200,
                "data": p
            }
        ), 200
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    }, 400)

@app.route("/userproperties", methods=["POST"])
def getUserProperties():
    jsonData = request.get_json()
    print(jsonData)
    if(jsonData["userId"] != None):
        propertyList = dbconnector.select_all_parameters("SELECT * FROM Property WHERE userId = %s", (jsonData["userId"],))
        return jsonify({
                "code": 200,
                "data": propertyList
            }
        ), 200
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    }, 400)

@app.route("/properties")
def get_all():
    propertyList = dbconnector.select_all("SELECT * FROM Property")
    return jsonify({
            "code": 200,
            "data": propertyList
        }
    ), 200

@app.route("/listings")
def get_newProperties():
    newlyAddedPropertyList = dbconnector.select_all("SELECT * FROM Property WHERE status = 'Available' ORDER BY dateCreated DESC;")
    newPropertyList = dbconnector.select_all("SELECT * FROM Property WHERE status = 'Available' ORDER BY leaseCommencementDate DESC;")
    hdbPropertyList = dbconnector.select_all("SELECT * FROM Property WHERE status = 'Available' AND propertyType = 'HDB' ORDER BY dateCreated DESC;")
    condoPropertyList = dbconnector.select_all("SELECT * FROM Property WHERE status = 'Available' AND propertyType IN ('Condominium', 'Executive Condo') ORDER BY dateCreated DESC;")
    landedPropertyList = dbconnector.select_all("SELECT * FROM Property WHERE status = 'Available' AND propertyType IN ('Cluster House', 'Semi-Detached House', 'Terraced House', 'Bungalow') ORDER BY dateCreated DESC;")
    
    return jsonify({
            "code": 200,
            "data": [
                {
                    "listingsId": "L10001",
                    "title": "Newly added",
                    "propertyList": newlyAddedPropertyList
                },
                {
                    "listingsId": "L10002",
                    "title": "New properties",
                    "propertyList": newPropertyList
                },
                {
                    "listingsId": "L10003",
                    "title": "HDB",
                    "propertyList": hdbPropertyList
                },
                {
                    "listingsId": "L10004",
                    "title": "Private Apartments",
                    "propertyList": condoPropertyList
                },
                {
                    "listingsId": "L10005",
                    "title": "Landed",
                    "propertyList": landedPropertyList
                }
                
            ]
        }
    ), 200

@app.route("/search", methods=['POST'])
def search():
    jsonData = request.get_json()
    print(jsonData)

    clauseList = ["status = 'Available'"]

    
    if "query" in jsonData:
        query = jsonData["query"]
        query = f"SELECT * FROM Property WHERE title LIKE '%{query}%' ORDER BY dateCreated DESC;"
        print(query)
        propertyList = dbconnector.select_all(query)
        return jsonify({
                "code": 200,
                "data": propertyList
            }
        ), 200

    ageStart = jsonData["ageStart"]
    if(ageStart != None and isinstance(ageStart, numbers.Number)):
        clauseList.append(f"TIMESTAMPDIFF(YEAR, leaseCommencementDate, NOW()) >= {ageStart}")

    ageEnd = jsonData["ageEnd"]
    if(ageEnd != None and isinstance(ageEnd, numbers.Number)):
        clauseList.append(f"TIMESTAMPDIFF(YEAR, leaseCommencementDate, NOW()) <= {ageEnd}")

    priceStart = jsonData["priceStart"]
    if(priceStart != None and isinstance(priceStart, numbers.Number)):
        clauseList.append(f"startingPrice >= {priceStart}")
    
    priceEnd = jsonData["priceEnd"]
    if(priceEnd != None and isinstance(priceEnd, numbers.Number)):
        clauseList.append(f"startingPrice <= {priceEnd}")

    propertyType = jsonData["propertyType"]
    if(propertyType != None):
        clauseList.append(f"propertyType = '{propertyType}'")

    query = f"SELECT * FROM Property WHERE {' AND '.join(clauseList)} ORDER BY dateCreated DESC;"
    print("Search query: " + query)

    propertyList = dbconnector.select_all(query)
    return jsonify({
            "code": 200,
            "data": propertyList
        }
    ), 200

@app.route('/create', methods=['POST'])
def create():
    jsonData = request.get_json()
    print(jsonData)
    query = "INSERT INTO Property(propertyType, title, description, postalCode, startingPrice, status, termOfLease, dateOfPurchase, leaseCommencementDate, sizeSQFT, fullAddress, noOfRooms, noOfToilets, dateCreated, userId) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)"
    params = (jsonData["propertyType"], jsonData["title"], jsonData["description"], jsonData["postalCode"], jsonData["startingPrice"], jsonData["status"], jsonData["termOfLease"], jsonData["dateOfPurchase"], jsonData["leaseCommencementDate"], jsonData['sizeSQFT'], jsonData["fullAddress"], jsonData["noOfRooms"], jsonData["noOfToilets"], jsonData["userId"])
    
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

@app.route('/edit', methods=['POST'])
def edit():
    jsonData = request.get_json()
    print(jsonData)
    query = "UPDATE Property SET propertyType = %s, title = %s, description = %s, postalCode = %s, startingPrice = %s, status = %s, termOfLease = %s, dateOfPurchase = %s, leaseCommencementDate = %s, sizeSQFT = %s, fullAddress = %s, noOfRooms = %s, noOfToilets = %s, userId = %s WHERE propertyId=%s"
    params = (jsonData["propertyType"], jsonData["title"], jsonData["description"], jsonData["postalCode"], jsonData["startingPrice"], jsonData["status"], jsonData["termOfLease"], jsonData["dateOfPurchase"], jsonData["leaseCommencementDate"], jsonData['sizeSQFT'], jsonData["fullAddress"], jsonData["noOfRooms"], jsonData["noOfToilets"], jsonData["userId"], jsonData['propertyid'])
    
    id = dbconnector.insert_parameters(query, params)
    print(f"Updated {id}")
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
            "message": "Unable to update."
        }
    ), 500


# @app.route('/buy', methods = ['POST'])
# def buy():
#     data = request.get_json()
#     property_1 = Property.query.filter_by(propertyid=data['propertyid']).first()
#     property_1.status = 'Sold'
#     db.session.commit()
#     return str(property_1.json())



if __name__ == '__main__':
    app.run(port=8002, debug=True)