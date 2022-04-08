import pymongo, urllib, os
from pymongo import MongoClient
from bson.objectid import ObjectId

DATABASE = os.environ['DATABASE_MONGODB_NAME']

mongo_url = f'mongodb+srv://btax:{urllib.parse.quote("#bt&i@$6")}@clustermasterbtax24.letri.mongodb.net/btax?retryWrites=true&w=majority'
client = MongoClient(mongo_url)

def get_database():
    return client[DATABASE]

def get_collection(collection_name):
    db = get_database()
    return db[collection_name]

def filtra_objs(collection_name, query):
    collection = get_collection(collection_name)
    return collection.find(query)

def get_obj(collection_name, query, fields=None):
    collection = get_collection(collection_name)
    return collection.find_one(query, fields)

def get_obj_by_id(collection_name, obj_id, fields=None):
    collection = get_collection(collection_name)
    return collection.find_one({'_id': ObjectId(obj_id)}, fields)

def get_first_obj(collection_name, query, fields, field_order, desc=False):
    collection = get_collection(collection_name)
    return collection.find_one(
        query,
        fields,
        sort=[(field_order, pymongo.DESCENDING if desc else pymongo.ASCENDING)]
    )

def inserir_obj(collection_name, obj):  
    collection = get_collection(collection_name)
    obj_id = collection.insert_one(obj).inserted_id
    return obj_id

def inserir_varios_objs(collection_name, lista_objs):
    collection = get_collection(collection_name)
    objs_ids = collection.insert_many(lista_objs)
    return objs_ids

def update_obj(collection_name, obj_id, obj):
    collection = get_collection(collection_name)
    values_update = {
        '$set': obj,
    }
    collection.update_one({'_id': ObjectId(obj_id)}, values_update)

def delete_obj(collection_name, obj_id):
    collection = get_collection(collection_name)
    collection.delete_one({'_id': ObjectId(obj_id)})

def delete_varios_objs(collection_name, query):
    collection = get_collection(collection_name)
    qtde = collection.delete_many(query)
    return qtde
