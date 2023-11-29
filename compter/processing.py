def NDVI(image):
    """
    Returns the NDVI of an image.
    """
    R = image[:,:,0].astype(float)
    IR = image[:,:,3].astype(float)
    NDVI = (IR - R) / (IR + R + 1e-6)
    return NDVI

def threshold(image, threshold=0):
    """
    Returns the image with the pixels below the threshold set to 0.
    """
    nv_image=image.copy()
    nv_image[nv_image < threshold] = 0
    return nv_image
