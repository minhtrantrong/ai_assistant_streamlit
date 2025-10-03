import pymongo
import config.config as config

client = pymongo.MongoClient(config.MONGO_DB_URL) 
db = client[config.MONGO_DB_NAME] 

def get_collection(name: str): 
    return db[name]