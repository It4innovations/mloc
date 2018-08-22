from bson import ObjectId

from auth import hash_password


def setup_db_hooks(app):
    def before_insert_user(users):
        for user in users:
            user['password'] = hash_password(user['password'])
        return users

    app.on_insert_users += before_insert_user


class Database:
    def __init__(self, app):
        self.db = app.data.driver.db

    def find_item(self, resource, field_name, field_value):
        return self.db[resource].find_one({field_name: field_value})

    def find_item_by_id(self, resource, item_id):
        return self.find_item(resource, '_id', ObjectId(item_id))

    def update_item(self, resource, item_id, update):
        return self.db[resource].find_one_and_update({'_id': ObjectId(item_id)}, {'$set': update})

    def create_item(self, resource, item):
        item['_id'] = self.db[resource].insert_one(item).inserted_id
        return item
