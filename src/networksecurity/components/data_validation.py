import os
import sys


from scipy.stats import ks_2samp
import pandas as pd


from networksecurity.entity import (
    DataIngestionArtifact,
    DataValidationConfig,
    DataValidationArtifact,
)
from networksecurity.utils import read_yaml_file, write_yaml_file
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

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Actual number of columns: {len(dataframe.columns)}")
            return number_of_columns == len(dataframe.columns)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05
    ) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold < is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column: {
                            "p_value": float(is_same_dist.pvalue),
                            "drift_status": is_found,
                        }
                    }
                )

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(
                file_path=drift_report_file_path, content=report, replace=True
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Initiating data validation process.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            logger.info("Reading data from train and test files")
            train_dataframe = DataValidation.read_data(file_path=train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)

            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train Dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test Dataframe does not contain all columns.\n"
            status = self.detect_dataset_drift(
                base_df=train_dataframe, current_df=test_dataframe
            )
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=True,
                header=True,
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=True,
                header=True,
            )
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
