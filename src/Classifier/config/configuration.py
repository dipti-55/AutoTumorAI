from Classifier.constants import *
import os
from Classifier.utils.common import read_yaml, create_directories,save_json
from Classifier.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig)


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
    

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        """
        Retrieves and prepares configuration specific to preparing the base model.

        Returns:
            PrepareBaseModelConfig: Configuration object for preparing the base model.
        """
        config = self.config.prepare_base_model # Retrieve configuration specific to preparing the base model
        
        create_directories([config.root_dir]) # Ensure prepare base model root directory exists

        # Construct a PrepareBaseModelConfig object using retrieved configuration and parameters
        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config