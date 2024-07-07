import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from Classifier.entity.config_entity import EvaluationConfig
from Classifier.utils.common import read_yaml, create_directories,save_json
import dagshub
dagshub.init(repo_owner='dipti-55', repo_name='Automated-Tumor-Detection', mlflow=True)


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        # Initialize Evaluation with the provided configuration
        self.config = config

    
    def _valid_generator(self):
        # Define parameters for the data generator
        datagenerator_kwargs = dict(
            rescale = 1./255, # Rescale pixel values from [0, 255] to [0, 1]
            validation_split=0.30 # Split the data for validation
        )

        # Define parameters for the data flow
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        # Create validation data generator
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

         # Create validation data flow from directory
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data, # Path to training data
            subset="validation", # Use validation subset
            shuffle=False, # Do not shuffle the data
            **dataflow_kwargs
        )


    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        # Load the trained model from the specified path
        return tf.keras.models.load_model(path)
    

    def evaluation(self):
        # Load the model using the configured path
        self.model = self.load_model(self.config.path_of_model)
        # Prepare the validation data generator
        self._valid_generator()
        # Evaluate the model on the validation data
        self.score = self.model.evaluate(self.valid_generator)
        # Save the evaluation score
        self.save_score()

    def save_score(self):
        # Save the evaluation scores to a JSON file
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)

    
    def log_into_mlflow(self):
        # Set the MLflow registry URI
        mlflow.set_registry_uri(self.config.mlflow_uri)
        # Determine the tracking URL type store
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        with mlflow.start_run():
            # Log all evaluation parameters to MLflow
            mlflow.log_params(self.config.all_params)
            # Log evaluation metrics (loss and accuracy) to MLflow
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            # Check if the tracking URL type store is not a file
            if tracking_url_type_store != "file":

                # Register the model in the MLflow Model Registry
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
            else:
                # Log the model without registering if using a file store
                mlflow.keras.log_model(self.model, "model")
