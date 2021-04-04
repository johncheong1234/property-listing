from flask import Flask, request,jsonify
import json
from flask_cors import CORS
import dbconnector

app = Flask(__name__)
CORS(app)

@app.route("/transactions")
def get_all():
    transactionlist = dbconnector.select_all("SELECT * FROM Transactions")
    if len(transactionlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": transactionlist
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no transactions."
        }
    ), 404


@app.route('/create', methods=['POST'])
def create():
    jsonData = request.get_json()
    print(jsonData)
    query = "INSERT INTO Property(propertyid, amount, sellerid, buyerid) VALUE(%s,%s,%s,%s)"
    params = (jsonData["propertyid"],jsonData["amount"],jsonData["sellerid"],jsonData["buyerid"])
  
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

    # try:
        # db.session.add(transaction)
        # db.session.commit()
    # except:
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "amount": transaction_data['amount'],
    #                 "buyerid": transaction_data['buyerid'],
    #                 "propertyid": transaction_data['propertyid'],
    #                 "sellerid": transaction_data['sellerid']
    #             },
    #             "message": "An error occurred creating the property listing."
    #         }
    #     ), 500
 
    #return jsonify(
    #    {
    #        "code": 201,
    #        "data": transaction.json()
    #    }
    #), 201

if __name__ == '__main__':
    app.run(port=8003, debug=True)
