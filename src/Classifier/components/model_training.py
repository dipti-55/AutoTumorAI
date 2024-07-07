import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
import time
from pathlib import Path
from Classifier.entity.config_entity import TrainingConfig


class Training:
    def __init__(self, config):
        # Initialize with the provided configuration
        self.config = config
        self.model = None
        self.train_generator = None
        self.valid_generator = None

    def get_base_model(self):
        # Load the base model from the specified path
        try:
            self.model = tf.keras.models.load_model(self.config.updated_base_model_path)
            print(f"Model loaded from {self.config.updated_base_model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e

    def train_valid_generator(self):
        # Parameters for the data generator
        datagenerator_kwargs = {
            'rescale': 1./255,  # Rescale pixel values from [0, 255] to [0, 1]
            'validation_split': 0.20 # Split the data into training and validation sets
        }
        
        # Parameters for the data flow
        dataflow_kwargs = {
            'target_size': tuple(self.config.params_image_size[:-1]), # Target image size
            'batch_size': self.config.params_batch_size, # Batch size
            'interpolation': 'bilinear' # Interpolation method for resizing images
        }

    
        # Create validation data generator
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)

        # Create validation data flow
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset='validation',
            shuffle=False,
            **dataflow_kwargs
        )

         # Create training data generator with augmentation if enabled
        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator # Use the same data generator as validation

        # Create training data flow
        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset='training',
            shuffle=True,
            **dataflow_kwargs
        )

        # Print the number of samples in training and validation sets
        print(f"Number of training samples: {self.train_generator.samples}")
        print(f"Number of validation samples: {self.valid_generator.samples}")

    @staticmethod
    def save_model(path, model):
        # Save the trained model to the specified path
        model.save(path)
        print(f"Model saved at {path}")

    def train(self):
        try:
            # Load the base model
            self.get_base_model()
            # Prepare data generators for training and validation
            self.train_valid_generator()
            
            # Define the optimizer with the specified learning rate
            optimizer = tf.keras.optimizers.SGD(learning_rate=self.config.params_learning_rate)

            # Compile the model with loss function and metrics
            self.model.compile(
                optimizer=optimizer,
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=['accuracy']
            )

            print("Model compiled successfully")

            # Train the model for the specified number of epochs
            for epoch in range(self.config.params_epochs):
                print(f"Epoch {epoch + 1}/{self.config.params_epochs}")
                history = self.model.fit(
                    self.train_generator,
                    steps_per_epoch=self.train_generator.samples // self.config.params_batch_size,
                    validation_data=self.valid_generator,
                    validation_steps=self.valid_generator.samples // self.config.params_batch_size
                )

                # Check if training history is None
                if history is None:
                    raise ValueError("Training history is None. This might indicate an issue with the data generators.")

                print(f"Training completed successfully for epoch {epoch + 1}")

            # Save the trained model
            self.save_model(self.config.trained_model_path, self.model)

        except Exception as e:
            # Print error if an exception occurs during training
            print(f"An error occurred during model training: {e}")
            raise e
