from bson.objectid import ObjectId

def validate_OId(id_str):
    return ObjectId.is_valid(id_str)
