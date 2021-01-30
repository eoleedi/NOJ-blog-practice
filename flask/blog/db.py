import os
from pymongo import MongoClient


    
client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@mongodb:27017/')

def get_db():
    db = client[os.environ['MONGODB_DATABASE']]
    return db


    
