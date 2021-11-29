# Utility functions

# Author: Marco Huber, 2020
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de

import os

def image_iter(path):
    """
    Takes path to a folder of images and returns every image path as
    string.
    
    Parameters
    ----------
    path : str
        The path of the folder.

    Returns
    -------
    image_paths : list of image paths
        List containing the path to every single image.

    """
    image_paths = []
   
    for path, subdirs, files in os.walk(path):
        for name in files:
            image_paths.append(os.path.join(path, name))
    
    return image_paths

