def NDVI(image):
    R = image[:,:,0].astype(float)
    IR = image[:,:,3].astype(float)
    NDVI = (IR - R) / (IR + R + 1e-6)
    return NDVI