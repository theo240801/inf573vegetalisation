import matplotlib.pyplot as plt
import numpy as np

def elevation(image):
    """
    Returs the elevation channel of a five channel image.
    """
    return image[:,:,4]

def IR(image):
    """
    Returns the IR channel of a five channel image.
    """
    return image[:,:,3]


def RGB(image):
    """
    Returns the RGB of a five channel image.
    """
    R = image[:,:,0]
    G = image[:,:,1]
    B = image[:,:,2]
    RGB = np.stack((R, G, B), axis=-1)
    return RGB

def NDVI(image):
    """
    Returns the NDVI of a five channel image.
    """
    R = image[:,:,0].astype(float)
    IR = image[:,:,3].astype(float)
    NDVI = (IR - R) / (IR + R + 1e-6)
    return NDVI



def binary_threshold(image, threshold_min=0, threshold_max=1e7):
    """
    Returns the image with the pixels below the threshold set to 0.
    """
    binary = np.zeros_like(image)
    binary[image > threshold_min] = 1
    binary[image > threshold_max] = 0
    return binary

def binary_map(image):
    """
    Applies the binary threshold about both the elevation and the NDVI on a given 5 channel image.
    """
    ndvi = NDVI(image)
    elev = elevation(image)
    binary = np.zeros_like(ndvi)
    binary[ndvi > 0.2] = 1
    binary[elev > 20] = 0
    return binary
