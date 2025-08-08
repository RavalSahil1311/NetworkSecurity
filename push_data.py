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
        except Exception as e:
            raise NetworkSecurityException(e, sys)
