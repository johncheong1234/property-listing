from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import dbconnector

app = Flask(__name__)
CORS(app)

@app.route("/activeauction", methods=["POST"]) #Used by anyone (The newest auction)
def getActiveAuctionForProperty():
    jsonData = request.get_json()
    print(jsonData)
    
    if "propertyId" in jsonData:
        propertyId = jsonData["propertyId"]

        query = "SELECT * FROM Auction WHERE propertyId = %s ORDER BY startDate DESC LIMIT 1;"
        params = (propertyId, )
        auction = dbconnector.select_one_parameters(query, params)
        bids = []

        #Obtain bids
        if auction != None:
            query = "SELECT * FROM Bid WHERE auctionId = %s ORDER BY amount DESC LIMIT 5;"
            params = (auction["auctionId"], )
            bids = dbconnector.select_all_parameters(query, params)
        
        return jsonify({
                "code": 200,
                "data": {
                    "auction": auction,
                    "bids": bids
                }
            }
        )
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    })
    
@app.route("/auctions", methods=["POST"]) #Used by the owner to see the list of auctions he sets up
def getAuctionForProperty():
    jsonData = request.get_json()
    print(jsonData)
    
    if "propertyId" in jsonData:
        propertyId = jsonData["propertyId"]

        query = "SELECT a.*, (SELECT amount FROM Bid b WHERE b.auctionId = a.auctionId ORDER BY amount DESC LIMIT 1) AS 'highestBidAmount' FROM Auction a WHERE propertyId = %s ORDER BY startDate DESC;"
        params = (propertyId, )
        auctionList = dbconnector.select_all_parameters(query, params)

        return jsonify({
                "code": 200,
                "data": auctionList
            }
        )
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    })

#Create auction
@app.route('/create', methods=['POST'])
def create():
    jsonData = request.get_json()
    print(jsonData)
    
    if "propertyId" in jsonData and "startDate" in jsonData and "endDate" in jsonData:
        if eligibleToCreate(jsonData["propertyId"]) == False:
            return jsonify({
                "code": 500,
                "message": "Not eligible to create auction"
            })
        #Insert   
        query = "INSERT INTO Auction(propertyId, startDate, endDate, dateCreated) VALUE(%s, %s, %s, NOW())"
        params = (jsonData["propertyId"], jsonData["startDate"], jsonData["endDate"])
        
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
        "message": "Invalid parameters."
    })

def eligibleToCreate(propertyId):
    # Must not have an auction running for that property & most not have any bids
    query = "SELECT * FROM Auction WHERE propertyId = %s AND NOW() >= startDate AND NOW() <= endDate;"
    params = (propertyId, )
    auctionList = dbconnector.select_all_parameters(query, params)
    if(len(auctionList) > 0):
        return False
    query = "SELECT a.* FROM Auction a INNER JOIN Bid b ON a.auctionId = b.auctionId WHERE propertyId = %s;"
    params = (propertyId, )
    auctionList = dbconnector.select_all_parameters(query, params)
    if(len(auctionList) > 0):
        return False
    return True


#Get get user's bid amount
@app.route('/currentbid', methods=['POST'])
def currentBid():
    jsonData = request.get_json()
    print(jsonData)
    if "propertyId" in jsonData and "userId" in jsonData:
        query = "SELECT b.* FROM Auction a INNER JOIN Bid b ON a.auctionId = b.auctionId WHERE propertyId = %s AND userId = %s ORDER BY b.dateCreated DESC LIMIT 1;"
        params = (jsonData["propertyId"], jsonData["userId"])
        bid = dbconnector.select_one_parameters(query, params)
        return jsonify(
            {
                "code": 200,
                "data": bid
            }
        ), 200
    return jsonify({
        "code": 400,
        "message": "Invalid parameters."
    }), 400

#Set bids
@app.route('/bid', methods=['POST'])
def setBid():
    jsonData = request.get_json()
    print(jsonData)
    if "amount" in jsonData and "propertyId" in jsonData and "userId" in jsonData:
        auction = eligibleToBid(jsonData["propertyId"], jsonData["amount"])
        if auction == None:
            return jsonify({
                "code": 500,
                "message": "Not eligible to create bid"
            }), 500
        #Insert   
        print("insert")
        query = "INSERT INTO Bid(amount, auctionId, userId, dateCreated) VALUE(%s, %s, %s, NOW())"
        params = (jsonData["amount"], auction["auctionId"], jsonData["userId"])
        
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
        "message": "Invalid parameters."
    }), 400

def eligibleToBid(propertyId, amount):
    # Auction must still be opened & more than the highest bid
    query = "SELECT * FROM Auction WHERE propertyId = %s AND NOW() >= startDate AND NOW() <= endDate AND closed = 0 ORDER BY startDate DESC LIMIT 1;"
    params = (propertyId, )
    auction = dbconnector.select_one_parameters(query, params)
    if(auction == None):
        return None
    query = "SELECT b.amount FROM Auction a INNER JOIN Bid b ON a.auctionId = b.auctionId WHERE a.propertyId = %s ORDER BY b.amount DESC LIMIT 1;"
    params = (propertyId, )
    bid = dbconnector.select_one_parameters(query, params)
    if(bid == None or bid["amount"] < amount):
        return auction
    else:
        return None

if __name__ == '__main__':
    app.run(port=8009, debug=True)