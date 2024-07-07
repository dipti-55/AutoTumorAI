from Classifier.config.configuration import ConfigurationManager
from Classifier.components.data_ingestion import DataIngestion
from Classifier import logger

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    """
    DataIngestionTrainingPipeline class manages the data ingestion stage of the training pipeline.

    Attributes:
        None
    """
    def __init__(self):
        """
        Constructor method for DataIngestionTrainingPipeline class.
        """
        pass

    def main(self):
        """
        Main method to execute the data ingestion stage.

        Args:
            None

        Returns:
            None
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()



if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
