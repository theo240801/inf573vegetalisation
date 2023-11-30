import matplotlib.pyplot as plt
import numpy as np
import cv2

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

def binary_map(image, minNDVI=0.2, maxElev=20):
    """
    Applies the binary threshold about both the elevation and the NDVI on a given 5 channel image.
    """
    ndvi = NDVI(image)
    elev = elevation(image)
    binary = np.zeros_like(ndvi)
    binary[ndvi > minNDVI] = 1
    binary[elev > maxElev] = 0
    return binary


def extract_connected_components(image, min_size):
    """
    Extracts the connected components of a binary image.
    """
    image_reformated = np.uint8(image)
    # Find connected components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image_reformated, connectivity=8)
    # Extract sizes and update the number of components
    sizes = stats[1:, -1]
    nb_components -= 1
    # Initialize the answer image
    connected_components_img = np.zeros_like(image_reformated)
    # Keep components above the minimum size
    for i in range(nb_components):
        if sizes[i] >= min_size:
            connected_components_img[output == i + 1] = 255
    
    return connected_components_img, nb_components, output


def highlight_max_ndvi_component(image, square_size=3, min_size=50):
    """
    Returns the image with the maximum NDVI value in each connected component colored.
    """
    # Initialiser l'image résultante en noir et blanc (img_result)
    ndvi = NDVI(image)
    img_filtered = extract_connected_components(binary_map(image), min_size=min_size)[0]
    img_result = np.zeros_like(ndvi)
    
    nb_components, output, _, _ = cv2.connectedComponentsWithStats(img_filtered, connectivity=8)

    # Parcourir chaque composant connecté
    for i in range(1, nb_components):
        # Initialiser une image pour le composant connecté courant
        img_result2 = np.zeros_like(ndvi)
        
        # Créer un masque pour le composant connecté
        component_mask = (output == i)
        
        # Remplir l'image img_result2 avec les valeurs NDVI du composant connecté
        img_result2[component_mask] = ndvi[component_mask]

        # Trouver les coordonnées (i, j) du pixel avec la valeur maximale dans le composant connecté
        max_ndvi_coord = np.unravel_index(np.argmax(img_result2), img_result2.shape)

        # Mettre à jour l'image résultante avec la valeur maximale
        img_result[max_ndvi_coord] = ndvi[max_ndvi_coord]
        
        # Afficher un carré autour des coordonnées de la valeur maximale
        for i in range(max_ndvi_coord[0] - square_size, max_ndvi_coord[0] + square_size + 1):
            for j in range(max_ndvi_coord[1] - square_size, max_ndvi_coord[1] + square_size + 1):
                img_result[i, j] = ndvi[i, j]

    return img_result