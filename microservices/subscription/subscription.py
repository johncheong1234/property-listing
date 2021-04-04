from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import dbconnector

app = Flask(__name__)
CORS(app)


@app.route('/create', methods=['POST'])
def create():
    jsonData = request.get_json()
    print(jsonData)
    query = "INSERT INTO Subscription(ageStart, ageEnd, priceStart, priceEnd, propertyType, userId) VALUE(%s, %s, %s, %s, %s, %s)"
    params = (jsonData["ageStart"], jsonData["ageEnd"], jsonData["priceStart"], jsonData["priceEnd"], jsonData["propertyType"], jsonData["userId"])
    
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

@app.route("/user", methods=["POST"])
def getUsers():
    jsonData = request.get_json()
    print(jsonData)
    
    if "age" in jsonData and "price" in jsonData and "propertyType" in jsonData:
        age = jsonData["age"]
        price = jsonData["price"]
        propertyType = jsonData["propertyType"]

        query = """
            SELECT userId FROM Subscription
            WHERE (
                (ageStart IS NULL AND ageEnd IS NULL) OR
                (ageStart IS NOT NULL AND ageStart IS NOT NULL AND ageStart >= %s AND ageEnd <= %s) OR
                (ageStart IS NOT NULL AND ageEnd IS NULL AND ageStart >= %s) OR
                (ageEnd IS NOT NULL AND ageStart IS NULL AND  ageEnd <= %s)
            ) AND (
                (priceStart IS NULL AND priceEnd IS NULL) OR
                (priceStart IS NOT NULL AND priceStart IS NOT NULL AND priceStart >= %s AND priceEnd <= %s) OR
                (priceStart IS NOT NULL AND priceEnd IS NULL AND priceStart >= %s) OR
                (priceEnd IS NOT NULL AND priceStart IS NULL AND  priceEnd <= %s)
            ) AND (
                propertyType IS NULL OR propertyType = '%s'
            );
        """
        params = (age, age, age, age, price, price, price, price, propertyType)
        userIdList = dbconnector.select_all_parameters(query, params)
        return jsonify({
                "code": 200,
                "data": [1,2,3]
            }
        ), 200
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    }, 400)


# @app.route("/subscriptions")
# def get_all():
#     subscriptionlist = Subscription.query.all()
#     if len(subscriptionlist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "subscriptions": [subscription.json() for subscription in subscriptionlist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no subscriptions."
#         }
#     ), 404

# @app.route("/subscriptions/<string:propertytype>",methods=['POST','GET'])
# def get_subscriptions_by_propertytype(propertytype):
#     subscriptionlist = db.session.query(Subscription).filter(Subscription.propertytype == propertytype)

#     if (subscriptionlist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "subscriptions": [subscription.json() for subscription in subscriptionlist]
#                 }
#             }
#         )

if __name__ == '__main__':
    app.run(port=8004, debug=True)