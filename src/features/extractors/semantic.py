import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image as kimage
from tensorflow.keras.models import Model

class SemanticExtractor:
    def __init__(self):
        print("Loading ResNet50 Model... (This may take a while)")
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        self.model = base_model

    def extract(self, image_path):
        try:
            img = kimage.load_img(image_path, target_size=(224, 224))
            x = kimage.img_to_array(img)
            
            x = np.expand_dims(x, axis=0)
            
            x = preprocess_input(x)

            features = self.model.predict(x, verbose=0)
            
            return features[0].tolist()

        except Exception as e:
            print(f"Error extracting semantic for {image_path}: {e}")
            return [0.0] * 2048