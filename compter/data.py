from PIL import Image
import random
import matplotlib.pyplot as plt
import rasterio
from matplotlib.colors import hex2color
import numpy as np
from pathlib import Path
import cv2


def get_data_paths (path, filter):
    """
    Gets the path of the images.
    """
    for path in Path(path).rglob(filter):
         yield path.resolve().as_posix()

def display_samples(images,nb_samples: list) -> None:
    """
    Shows random images of the flair dataset
    """
    indices= random.sample(range(0, len(images)), nb_samples)
    fig, axs = plt.subplots(nrows = nb_samples, ncols = 6, figsize = (20, nb_samples * 6)); fig.subplots_adjust(wspace=0.0, hspace=0.01)
    fig.patch.set_facecolor('black')
    for u, idx in enumerate(indices):
        with rasterio.open(images[idx], 'r') as f:
            im = f.read([1,2,3]).swapaxes(0, 2).swapaxes(0, 1)
            imir = f.read([4])[0]
            imel = f.read([5])[0]
            imr= f.read([1])[0]
            img= f.read([2])[0]
            imb= f.read([3])[0]
        ax0 = axs[u][0] ; ax0.imshow(im);ax0.axis('off')
        ax1 = axs[u][1] ; ax1.imshow(imir);ax1.axis('off')
        ax2 = axs[u][2] ; ax2.imshow(imel);ax2.axis('off')
        ax3 = axs[u][3] ; ax3.imshow(imr);ax3.axis('off')
        ax4 = axs[u][4] ; ax4.imshow(img);ax4.axis('off')
        ax5 = axs[u][5] ; ax5.imshow(imb);ax5.axis('off')
        if u == 0:
            ax0.set_title('RVB Image', size=16,fontweight="bold",c='w')
            ax1.set_title('NIR Image', size=16,fontweight="bold",c='w')
            ax2.set_title('Elevation', size=16,fontweight="bold",c='w')
            ax3.set_title('Red', size=16,fontweight="bold",c='w')
            ax4.set_title('Green', size=16,fontweight="bold",c='w')
            ax5.set_title('Blue', size=16,fontweight="bold",c='w')
    for i in indices:
        print(images[i])

def read_image(path):
    """Gets the numpy array of an image from its path"""
    with rasterio.open(path, 'r') as f:
        imageR = f.read([1])[0]
        imageG = f.read([2])[0]
        imageB = f.read([3])[0]
        imageIR = f.read([4])[0]
        imageE = f.read([5])[0]
    image = np.stack([imageR, imageG, imageB, imageIR, imageE], axis=-1)
    return image
    
def imshow(image, cmap=None, vmin=None, vmax=None):
    """Display an image whether its number of channels is 1, 3 or 5"""
    if cmap is None:
        cmap = 'viridis'
    if vmin is None:    
        vmin = np.min(image)
    if vmax is None:
        vmax = np.max(image)
    if np.transpose(image).shape[0] == 5:
        return plt.imshow(image[:,:,0:3], cmap=cmap, vmin=vmin, vmax=vmax)
    else :
        return plt.imshow(image, cmap=cmap, vmin=vmin, vmax=vmax)
