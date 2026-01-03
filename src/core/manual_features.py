import numpy as np
from PIL import Image

def extract_color_hsv(image_path):
    img = Image.open(image_path).convert('HSV')
    img_arr = np.array(img)

    h_hist, edges = np.histogramdd(
        img_arr.reshape(-1, 3),
        bins=(8, 8, 8),
        range=((0, 256), (0, 256), (0, 256))
    )
    
    feature_vec = h_hist.flatten()
    feature_vec = feature_vec / (feature_vec.sum() + 1e-6)

    return feature_vec

def calculate_glcm_props(glcm):
    levels = glcm.shape[0]
    i, j = np.ogrid[0:levels, 0:levels]

    contrast = np.sum(glcm * (i - j)**2)
    energy = np.sum(glcm**2)
    homogeneity = np.sum(glcm / (1.0 + np.abs(i - j)))

    mu_i = np.sum(i * glcm)
    mu_j = np.sum(j * glcm)
    sigma_i = np.sqrt(np.sum((i - mu_i)**2 * glcm))
    sigma_j = np.sqrt(np.sum((j - mu_j)**2 * glcm))
    if sigma_i * sigma_j == 0:
        correlation = 0
    else:
        correlation = np.sum((i - mu_i) * (j - mu_j) * glcm) / (sigma_i * sigma_j)
        
    return [contrast, energy, homogeneity, correlation]

def extract_glcm(image_path):
    img = Image.open(image_path).convert('L').resize((64, 64))
    arr = np.array(img)

    levels = 16
    arr = (arr // (256 // levels)).astype(int)
    
    H, W = arr.shape
    glcm_features = []

    offsets = [(0, 1), (-1, 1), (-1, 0), (-1, -1)]
    for dy, dx in offsets:
        src = arr[max(0, -dy):min(H, H-dy), max(0, -dx):min(W, W-dx)]
        dst = arr[max(0, dy):min(H, H+dy), max(0, dx):min(W, W+dx)]
        
        glcm, _, _ = np.histogram2d(src.flatten(), dst.flatten(), bins=levels, range=[[0, levels], [0, levels]])
        glcm = glcm / (glcm.sum() + 1e-6)

        props = calculate_glcm_props(glcm)
        glcm_features.extend(props)
        
    return np.array(glcm_features)

def extract_sobel_grid(image_path):
    img = Image.open(image_path).convert('L').resize((128, 128))
    arr = np.array(img, dtype=np.float32)
    
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    tl = arr[:-2, :-2]; t = arr[:-2, 1:-1]; tr = arr[:-2, 2:]
    l  = arr[1:-1, :-2];                    r  = arr[1:-1, 2:]
    bl = arr[2:, :-2];  b = arr[2:, 1:-1];  br = arr[2:, 2:]

    Gx = (tr + 2*r + br) - (tl + 2*l + bl)
    Gy = (bl + 2*b + br) - (tl + 2*t + tr)

    magnitude = np.sqrt(Gx**2 + Gy**2)

    H_mag, W_mag = magnitude.shape
    h_step = H_mag // 4
    w_step = W_mag // 4
    
    features = []
    threshold = np.mean(magnitude)
    
    for i in range(4):
        for j in range(4):
            cell = magnitude[i*h_step:(i+1)*h_step, j*w_step:(j+1)*w_step]
            edge_pixels = np.sum(cell > threshold)
            total_pixels = cell.size
            density = edge_pixels / (total_pixels + 1e-6)
            
            features.append(density)
            
    return np.array(features)