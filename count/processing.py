import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.ndimage import maximum_filter
from scipy import stats
from scipy.ndimage.morphology import binary_dilation



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

def binary_map(image, minNDVI=0, maxElev=70, minElev=10):
    """
    Applies the binary threshold about both the elevation and the NDVI on a given 5 channel image.
    """
    ndvi = NDVI(image)
    elev = elevation(image)
    binary = np.zeros_like(ndvi)
    binary[ndvi > minNDVI] = 1
    binary[elev > maxElev] = 0
    binary[elev < minElev] = 0
    return binary

def indice(liste, element):
    for i in range(len(liste)):
        if liste[i] == element:
            return i
    return -1

def new_output(true_outputs, output):
    new_outputs =  []
    for i in range(1,len(true_outputs)+1):
        new_outputs.append(i)
    new_output = new_outputs[indice(true_outputs,output)]
    

def extract_connected_components(image, min_size=50):
    """
    Extracts the connected components of a binary image.
    image : binary image
    min_size : minimum size of the connected components to keep
    """
    binary = np.uint8(image.copy())
    # Find connected components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    # Extract sizes and update the number of components
    sizes = stats[1:, cv2.CC_STAT_AREA]
    nb_components -= 1
    # Initialize the answer image
    connected_components_img = np.zeros_like(binary)
    # Keep components above the minimum size
    true_component=[]
    true_outputs=[]
    real_nb_components = 0
    for i in range(1, nb_components+1):
        if sizes[i-1] >= min_size:
            connected_components_img[output == i] = 255
            real_nb_components += 1
            true_component.append(True)
        else:  
            true_component.append(False)

    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            if not(true_component[output[i,j]-1]):
                output[i,j]=0
            else : 
                if output[i,j] not in true_outputs:
                    true_outputs.append(output[i,j])

    possible_new_outputs =  []
    for i in range(1,len(true_outputs)+1):
        possible_new_outputs.append(i)

    new_outputs = np.zeros_like(output)
    for i in range(new_outputs.shape[0]):
        for j in range(new_outputs.shape[1]):
            if output[i,j]!=0:
                new_outputs[i,j] = possible_new_outputs[indice(true_outputs,output[i,j])]
    
    return connected_components_img, real_nb_components, new_outputs



def coords_max_ndvi_component(image, min_size=50):
    """
    Returns the image with the maximum NDVI value in each connected component colored.
    image : 5 channel image
    square_size : size of the square around the maximum value
    min_size : minimum size of the connected components to keep
    """
    # Initialiser l'image résultante en noir et blanc (img_result)
    ndvi = NDVI(image)
    img_filtered, nb_components, output = extract_connected_components(binary_map(image), min_size=min_size)
    
    coords = []
    # Parcourir chaque composant connecté
    for i in range(1, nb_components+1):
        # Initialiser une image pour le composant connecté courant
        img_result2 = np.zeros_like(ndvi)
        
        # Créer un masque pour le composant connecté
        component_mask = (output == i)
        
        # Remplir l'image img_result2 avec les valeurs NDVI du composant connecté
        img_result2[component_mask] = ndvi[component_mask]

        # Trouver les coordonnées (i, j) du pixel avec la valeur maximale dans le composant connecté
        max_ndvi_coord = np.unravel_index(np.argmax(img_result2), img_result2.shape)

        coords.append(max_ndvi_coord)

    return coords

def local_maximums(image, size=30):
    # Apply maximum filter to find local maxima
    local_maxima = maximum_filter(image, size) == image
    coords_local_maximum=[]
    local_maxima[image==0]=False
    for i in range(local_maxima.shape[0]):
        for j in range(local_maxima.shape[1]):
            if local_maxima[i,j]:
                coords_local_maximum.append((i,j))
    return coords_local_maximum

def local_maximums_of_ndvi_connexe_components(image,min_size=50, local_max_size=30):
    ndvi = NDVI(image)
    img_filtered, nb_components, output = extract_connected_components(binary_map(image), min_size=min_size)
    coords = []
    # Parcourir chaque composant connecté
    for i in range(1, nb_components+1):
        # Initialiser une image pour le composant connecté courant
        img_result2 = np.zeros_like(ndvi)
        # Créer un masque pour le composant connecté
        component_mask = (output == i)
        # Remplir l'image img_result2 avec les valeurs NDVI du composant connecté
        img_result2[component_mask] = ndvi[component_mask]
        coords += local_maximums(img_result2, size=local_max_size)
    return coords

def binary_masks_from_mask(msk, smoothing=15):
    binary_masks = []
    for i in range(1, 7):
        mask = msk == i
        dilated_mask = binary_dilation(mask, iterations=smoothing)  # Increase the iterations value for stronger dilation
        binary_masks.append(dilated_mask)
    return binary_masks


