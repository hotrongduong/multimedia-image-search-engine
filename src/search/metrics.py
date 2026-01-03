import numpy as np

def chi2_distance(histA, histB, eps=1e-10):
    histA = np.array(histA, dtype=float)
    histB = np.array(histB, dtype=float)
    
    d = 0.5 * np.sum(((histA - histB) ** 2) / (histA + histB + eps))
    return d

def euclidean_distance(vecA, vecB):
    vecA = np.array(vecA, dtype=float)
    vecB = np.array(vecB, dtype=float)
    
    return np.linalg.norm(vecA - vecB)

def cosine_distance(vecA, vecB):
    vecA = np.array(vecA, dtype=float)
    vecB = np.array(vecB, dtype=float)
    
    dot_product = np.dot(vecA, vecB)
    norm_a = np.linalg.norm(vecA)
    norm_b = np.linalg.norm(vecB)
    
    similarity = dot_product / (norm_a * norm_b + 1e-10)
    
    return 1.0 - similarity