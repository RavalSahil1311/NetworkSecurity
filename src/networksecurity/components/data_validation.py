import os
import sys


from scipy.stats import ks_2samp
import pandas as pd


from networksecurity.entity import (
    DataIngestionArtifact,
    DataValidationConfig,
    DataValidationArtifact,
)
from networksecurity.utils import read_yaml_file
from networksecurity import get_logger, NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

logger = get_logger(__name__)


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
