from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from extensions import bcrypt
from database import users_collection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return "auth working"

@auth_bp.route("/register", methods=["POST"])
def register_user():

    data = request.json

    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    users_collection.insert_one({
        "username": data["username"],
        "password": hashed_pw
    })

    return jsonify({"msg": "User created successfully"})


@auth_bp.route("/login", methods=["POST"])
def login_user():

    data = request.json

    user = users_collection.find_one({
        "username": data["username"]
    })

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if bcrypt.check_password_hash(
        user["password"],
        data["password"]
    ):

        token = create_access_token(
            identity=data["username"]
        )

        return jsonify({
            "token": token,
            "username": data["username"]
        })

    return jsonify({"msg": "Invalid credentials"}), 401