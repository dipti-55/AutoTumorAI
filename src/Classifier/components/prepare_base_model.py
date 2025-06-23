import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from Classifier.entity.config_entity import PrepareBaseModelConfig

"""
Prepares a VGG16-based model for tumor detection by loading pretrained weights, freezing base layers, adding a custom classification layer, compiling with SGD optimizer, and saving both the base and updated models at specified paths.
"""
class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    
    def get_base_model(self):
        # Load VGG16 model with specified parameters
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        # Save the base model to a specified path
        self.save_model(path=self.config.base_model_path, model=self.model)

    
    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        # Freeze layers based on configuration
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        # Add new dense layer for classification
        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(flatten_in)

        # Create a new model by combining the base model with the classification layer
        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        # Compile the full model with optimizer, loss function, and metrics
        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        # Print model summary
        full_model.summary()
        return full_model
    
    
    def update_base_model(self):
        # Prepare full model by adding classification layers and compiling
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True, # Freeze all layers of the base model
            freeze_till=None, # Do not freeze any specific layers
            learning_rate=self.config.params_learning_rate
        )

        # Save the updated full model to a specified path
        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        # Save the TensorFlow model to the specified path
        model.save(path)


