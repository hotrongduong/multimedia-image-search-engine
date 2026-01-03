import numpy as np
from PIL import Image

def extract_color_histogram(image_path, bins=(8, 12, 3)):
    try:
        img = Image.open(image_path).convert("RGB")
        img_array = np.array(img)

        img_array = img_array / 255.0
        
        r, g, b = img_array[..., 0], img_array[..., 1], img_array[..., 2]
        
        c_max = np.max(img_array, axis=2)
        c_min = np.min(img_array, axis=2)
        delta = c_max - c_min
        
        h = np.zeros_like(c_max)
        s = np.zeros_like(c_max)
        v = c_max 

        mask_delta = delta > 0
        
        mask_r = (c_max == r) & mask_delta
        h[mask_r] = ((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6
        
        mask_g = (c_max == g) & mask_delta
        h[mask_g] = ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2
        
        mask_b = (c_max == b) & mask_delta
        h[mask_b] = ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4
        
        h = h / 6.0

        mask_max = c_max > 0
        s[mask_max] = delta[mask_max] / c_max[mask_max]

        h_idx = (h * bins[0]).astype(int)
        s_idx = (s * bins[1]).astype(int)
        v_idx = (v * bins[2]).astype(int)

        h_idx = np.clip(h_idx, 0, bins[0] - 1)
        s_idx = np.clip(s_idx, 0, bins[1] - 1)
        v_idx = np.clip(v_idx, 0, bins[2] - 1)

        hist = np.zeros(bins, dtype=int)
        
        flat_indices = h_idx * (bins[1] * bins[2]) + s_idx * bins[2] + v_idx
        
        total_bins = bins[0] * bins[1] * bins[2]
        hist_flat = np.bincount(flat_indices.flatten(), minlength=total_bins)

        return hist_flat.tolist()

    except Exception as e:
        print(f"Error extracting color for {image_path}: {e}")
        return [0] * (bins[0] * bins[1] * bins[2])