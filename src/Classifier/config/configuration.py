from Classifier.constants import *
import os
from Classifier.utils.common import read_yaml, create_directories,save_json
from Classifier.entity.config_entity import DataIngestionConfig


# ConfigurationManager class manages configuration settings for the application.
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        """
        This is the constructor method that gets called when an instance of ConfigurationManager is created.

        Parameters: 
        config_filepath: The path to the configuration file (default is CONFIG_FILE_PATH).

        params_filepath: The path to the parameters file (default is PARAMS_FILE_PATH).
        """
        self.config = read_yaml(config_filepath) 
        self.params = read_yaml(params_filepath) 

        create_directories([self.config.artifacts_root]) # Ensure artifacts root directory exists


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves data ingestion configuration from ConfigurationManager.

        Returns:
            DataIngestionConfig: Configuration object for data ingestion.
        """
        config = self.config.data_ingestion # Extract data ingestion configuration from main config

        create_directories([config.root_dir]) # Ensure data ingestion root directory exists

        # Create DataIngestionConfig object using extracted configuration values
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )
        return data_ingestion_config