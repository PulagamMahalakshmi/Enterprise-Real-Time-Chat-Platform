from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)

db = client["chatapp"]

users_collection = db["users"]
messages_collection = db["messages"]