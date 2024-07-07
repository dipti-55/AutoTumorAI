from Classifier.constants import *
import os
from Classifier.utils.common import read_yaml, create_directories,save_json
from Classifier.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig, TrainingConfig)


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
    

    def get_training_config(self) -> TrainingConfig:
        """
        Retrieves and constructs training configuration parameters.

        Returns:
            TrainingConfig: An instance of TrainingConfig containing all necessary training parameters.
        """
        # Retrieve the training section from the configuration
        training = self.config.training
        # Retrieve the prepare_base_model section from the configuration
        prepare_base_model = self.config.prepare_base_model
        # Retrieve the parameters section from the configuration
        params = self.params

        # Construct the path to the training data directory
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "kidney2000")

        # Create directories for training artifacts
        create_directories([Path(training.root_dir)])

        # Create a TrainingConfig instance with the specified parameters
        training_config = TrainingConfig(
            root_dir=Path(training.root_dir), # Root directory for training artifacts
            trained_model_path=Path(training.trained_model_path), # Path to save the trained model
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path), # Path to the updated base model
            training_data=Path(training_data), # Path to the training data
            params_learning_rate=params.LEARNING_RATE, # Learning rate for training
            params_epochs=params.EPOCHS, # Number of epochs for training
            params_batch_size=params.BATCH_SIZE, # Batch size for training
            params_is_augmentation=params.AUGMENTATION, # Whether data augmentation should be used
            params_image_size=params.IMAGE_SIZE # Image size for the model input
        )

        return training_config 