import numpy as np
from PIL import Image
from skimage.feature import hog
from skimage.transform import resize

def extract_shape_hog(image_path, resize_shape=(128, 64)):
    try:
        img = Image.open(image_path).convert("L")
        img_array = np.array(img)

        resized_img = resize(img_array, resize_shape, anti_aliasing=True)

        hog_vector = hog(
            resized_img, 
            orientations=9, 
            pixels_per_cell=(8, 8), 
            cells_per_block=(2, 2), 
            block_norm='L2-Hys', 
            visualize=False
        )

        return hog_vector.tolist()

    except Exception as e:
        print(f"Error extracting shape for {image_path}: {e}")
        return []