import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity import NetworkSecurityException, get_logger
from networksecurity.entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig,
)

logger = get_logger(__name__)


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        dataingestion = DataIngestion(data_ingestion_config)
        logger.info("Initiate Data Ingestion")
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        logger.info("Data Ingestion completed successfully")
        logger.info("Initiate Data Validation")
        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data Validation completed successfully")
        logger.info(f"DATA_VALIDATION_ARTIFACT: {data_validation_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
