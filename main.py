import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity import NetworkSecurityException, get_logger
from networksecurity.entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
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
        logger.info("Initiate Data Transformation")
        data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config,
        )
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        logger.info("Data Transformation completed successfully")
        logger.info(f"DATA_TRANSFORMATION_ARTIFACT: {data_transformation_artifact}")
        logger.info("Initiate Model Trainer")
        model_trainer_config = ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config
        )
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_training()
        logger.info("Model Training completed successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
