from bson import ObjectId

def find_item(db, resource, item_id):
    item = db[resource].find_one({'_id': ObjectId(item_id)})
    if not item:
        abort(404)
    return item

def update_item(db, resource, item_id, update):
    db[resource].find_one_and_update({'_id': ObjectId(item_id)}, {'$set': update})
