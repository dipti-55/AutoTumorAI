import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Defining the predict_function with @tf.function
@tf.function(reduce_retracing=True)
def predict_function(model, input_data):
    return model(input_data)

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # Load model
        # model = load_model(os.path.join("model", "model.h5"))
        model = load_model(os.path.join("artifacts", "training", "model.h5"))

        # Load and preprocess the image
        imagename = self.filename
        test_image = image.load_img(imagename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        # Convert the image to a tensor
        test_image_tensor = tf.convert_to_tensor(test_image)

        # Using predict_function to make predictions
        result = np.argmax(predict_function(model, test_image_tensor), axis=1)
        print(result)

        # Interpret the result
        if result[0] == 1:
            prediction = 'Tumor'
            return [{"image": prediction}]
        else:
            prediction = 'Normal'
            return [{"image": prediction}]

if __name__ == "__main__":
    pipeline = PredictionPipeline("path_to_your_image.jpg")
    prediction = pipeline.predict()
    print(prediction)
