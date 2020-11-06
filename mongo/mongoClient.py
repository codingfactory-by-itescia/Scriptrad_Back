import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://root:rootpassword@127.0.0.1:27817')

#client = MongoClient('mongodb://root:rootpassword@127.0.0.1:80')
db = client.test