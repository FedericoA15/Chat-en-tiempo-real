from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Federico15:SbiAjuKOPquPdxA9@chattiemporeal.gtsgox0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.my_database


def get_database():
    return db
