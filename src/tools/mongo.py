from pymongo import MongoClient
import uuid



class MongoManager:
    def __init__(self, url:str):
        self.__client = MongoClient(url)

    def __get_collection(self, db_name, collection_name):
        db = self.__client[db_name]
        if not collection_name in db.list_collection_names(): 
            db.create_collection(collection_name)
        collection = db.get_collection(collection_name)
        return collection

    def upsert(self, db_name, collection_name, condition, query):
        collection = self.__get_collection(db_name, collection_name)
        result = collection.update(condition, query, upsert=True)
        return result
    
    def find_one(self, db_name, collection_name, condition):
        collection = self.__get_collection(db_name, collection_name)
        result = collection.find_one(condition)
        return result
