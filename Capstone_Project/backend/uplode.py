from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


# Function to upload data to MongoDB
def upload_to_mongodb(data: dict) -> str:
    try:
        client = MongoClient("mongodb+srv://T5:T5@cluster0.hc3il.mongodb.net/")
        db = client["database"]
        collection = db["database"]
        result = collection.insert_one(data)

        return f"Data uploaded successfully with ID: {result.inserted_id}"
    
    except ConnectionFailure:
        return "Failed to connect to MongoDB server."
    except Exception as e:
        return f"An error occurred: {str(e)}"