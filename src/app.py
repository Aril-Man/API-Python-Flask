import bcrypt
from flask import Flask, Response, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId, json_util


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/microDb"

mongo = PyMongo(app)

@app.route("/users/", methods=["POST"])
def create_user():

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    
    bytePwd = password.encode("utf-8")
    hashing = bcrypt.hashpw(bytePwd, bcrypt.gensalt())

    if username and email and password:
        id = mongo.db.users.insert_one(
            {
                "username": username, 
                "email": email, 
                "password": hashing
            })
        
        response = Response(
            json_util.dumps({
                "message": "User created successfully",
                "id": str(id.inserted_id),
                "username": username,
                "email": email,
                "password": hashing
                }), mimetype="application/json"
        )
        
        return response, 201
    else:
        return bad_request()
    
@app.route("/users/", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    
    return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(user)
    
    return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": "User " + id + " deleted successfully"})
    
    return response

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    
    mongo.db.users.find_one({"_id": ObjectId(id)})
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    
    bytePwd = password.encode("utf-8")
    hashing = bcrypt.hashpw(bytePwd, bcrypt.gensalt())
    
    if username and email and password:
        mongo.db.users.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username, 
                    "email": email, 
                    "password": hashing
                }
            }
        )
        response = Response(
            json_util.dumps({
                "message": "User " + id + " updated successfully",
                "id": str(id),
                "username": username,
                "email": email,
                "password": hashing
                }), mimetype="application/json"
        )
        
        return response, 201
    else:
        return bad_request()

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'status': 404,
        'message': 'Not Found: ' + request.url
    }) 
    
    response.status_code = 404
    return response

@app.errorhandler(400)
def bad_request(error=None):
    response = jsonify({
        'status': 400,
        'message': 'Bad Request: ' + request.url
    }) 
    
    response.status_code = 400
    return response
        
@app.route("/books/", methods=["POST"])
def create_book():
    
    title = request.json["title"]
    description = request.json["description"]
    owner = request.json["owner"]
    
    
    if title and description and owner:
        id = mongo.db.books.insert_one(
            {
                "title": title, 
                "description": description, 
                "owner": owner
            })
        
        response = {
            'message': 'Book created successfully',
            'data': {
                'id': str(id.inserted_id),
                'title': title,
                'description': description,
                'owner': owner
            }
        }

        return response, 201
    else:
        return bad_request()

@app.route("/books/", methods=["GET"])
def get_books():
    books = mongo.db.books.find()
    response = json_util.dumps(books)
    
    return Response(response, mimetype="application/json")

@app.route("/books/<id>", methods=["GET"])
def get_book(id):
    book = mongo.db.books.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(book)
    
    return Response(response, mimetype="application/json")

@app.route("/books/<id>", methods=["DELETE"])
def delete_book(id):
    mongo.db.books.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": "Book " + id + " deleted successfully"})
    
    return response

@app.route("/books/<id>", methods=["PUT"])
def update_book(id):
    mongo.db.books.find_one({"_id": ObjectId(id)})
    title = request.json["title"]
    description = request.json["description"]
    owner = request.json["owner"]
    
    if title and description and owner:
        mongo.db.books.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": title, 
                    "description": description, 
                    "owner": owner
                }
            }
        )
        response = {
            'message': 'Book '+ id +' updated successfully',
            'data': {
                'id': str(id),
                'title': title,
                'description': description,
                'owner': owner
            }
        }
        
        return response, 201
    else:
        return bad_request()

if __name__ == '__main__':
    app.run(debug=True)