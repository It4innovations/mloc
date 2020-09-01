import argparse

from pymongo import MongoClient

from .backends import LocalBackend
from .db import Database
from .model_manager import model_fit
from .settings import (MONGO_DBNAME, MONGO_HOST, MONGO_PASSWORD, MONGO_PORT,
                       MONGO_USERNAME)

parser = argparse.ArgumentParser(description='MLoC PBS Executor')
parser.add_argument('fit_id')
args = parser.parse_args()


fit_id = args.fit_id

client = MongoClient(MONGO_HOST,
                     MONGO_PORT,
                     username=MONGO_USERNAME,
                     password=MONGO_PASSWORD,
                     authSource=MONGO_DBNAME,
                     authMechanism='SCRAM-SHA-256')

db = client[MONGO_DBNAME]
db = Database(db)

data = {}
fit = db.find_item_by_id('fits', fit_id)
network = db.find_item_by_id('networks', fit['network_id'])
backend = LocalBackend(db, True)
backend.execute(model_fit, resource='fits', network=network, **fit)
