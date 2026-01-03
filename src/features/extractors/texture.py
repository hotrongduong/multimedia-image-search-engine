import numpy as np
from PIL import Image
from skimage.feature import local_binary_pattern

def extract_texture_lbp(image_path, points=8, radius=1, method='default'):
    try:
        img = Image.open(image_path).convert("L")
        img_array = np.array(img)

        lbp_image = local_binary_pattern(img_array, points, radius, method)

        if method == 'default':
            n_bins = 2**points  
        elif method == 'uniform':
            n_bins = points + 2 
        else:
            n_bins = 256 
            
        hist, _ = np.histogram(lbp_image.ravel(), bins=n_bins, range=(0, n_bins))

        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)  

        return hist.tolist()

    except Exception as e:
        print(f"Error extracting texture for {image_path}: {e}")
        return [0.0] * 256