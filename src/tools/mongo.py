from pymongo import MongoClient
import uuid



class MongoManager:
    def __init__(self, url:str):
        self.__client = MongoClient(url)

    def upsert(self, db_name, collection_name, condition, query):
        db = self.__client[db_name]
        if not collection_name in db.list_collection_names(): 
            db.create_collection(collection_name)
        collection = db.get_collection(collection_name)
        result = collection.update(condition, query, upsert=True)
        return result