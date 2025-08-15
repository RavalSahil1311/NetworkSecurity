import os
import sys
import pyaml


from networksecurity import get_logger, NetworkSecurityException


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return pyaml.yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
