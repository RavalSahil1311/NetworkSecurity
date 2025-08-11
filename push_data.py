import os
import sys
import json
import certifi
import pymongo

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from networksecurity import get_logger, NetworkSecurityException

load_dotenv()
logger = get_logger(__name__)

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongo(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.pymongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.pymongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    no_records = network_obj.insert_data_to_mongo(
        records=records,
        database=DATABASE,
        collection=COLLECTION,
    )
    print(f"Total records inserted: {no_records}")
