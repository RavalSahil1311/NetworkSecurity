import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity import NetworkSecurityException, get_logger
from networksecurity.entity import DataIngestionConfig, TrainingPipelineConfig

logger = get_logger(__name__)


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        dataingestion = DataIngestion(data_ingestion_config)
        logger.info("Initiate Data Ingestion")
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logger.info("Data Ingestion completed successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
