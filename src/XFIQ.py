# Explainable Face Image Quality (XFIQ)

# Pixel-Level Face Image Quality Assessment for Explainable Face Recognition
# Philipp Terhörst, Marco Huber, Naser Damer, Florian Kirchbuchner, Kiran Raja, and Arjan Kuijper
# 2021

# Author: Marco Huber, 2021
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de

import cv2
import numpy as np
import os.path
from tqdm import tqdm
from tensorflow.keras import models

from auxiliary_models import build_model
from serfiq import get_scaled_quality
from gradient_calculator import get_gradients
from utils import image_iter
from explain_quality import plot_comparison

def run(image_path, model_path, save_path, T):
    
    """
    Calculates the gradients using the calculated SER-FIQ image quality.

    Parameters
    ----------
    image_path : str
        Path to the image folder.
    model_path : str
        Path to the stored keras model.
    save_path : str
        Path to save the gradients.
    T : int
        Number of stochastic forward passes to calculate the SER-FIQ quality.
        
    Returns
    -------
    None. But saves the (image_path, gradients, quality score)

    """    

    # load model
    keras_model = models.load_model(model_path)
    
    # get images paths
    images = image_iter(image_path)
    
    save = []
    
    # calculating quality and gradients for each image
    for i in tqdm(images):
        
        # read & prepare image
        img = cv2.imread(i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (112, 112), interpolation = cv2.INTER_AREA)
        img = np.expand_dims(img, axis=0) 
        
        # calculate quality score
        score = get_scaled_quality(img, keras_model, T, alpha, r)
            
        # calculate gradient
        grads = get_gradients(img, keras_model, score)
        grads = grads.numpy()
        
        # add to save
        tmp = (i, grads, score)
        save.append(tmp)
        
    # save
    np.save(save_path, save)
    
if __name__ == "__main__":
    
    # SER-FIQ - Parameter
    T = 100         # number of forward passes to calculate quality
    
    # Quality Scaling - Parameters
    alpha = 130     # param to scale qualities to a wider range
    r = 0.88        # param to scale qualities to a wider range
    
    # Visualization Scaling - Parameters
    a = 10**7.5     # param to scale grads
    b = 2           # param to scale grads

    # Paths  
    weights_path = "interkerasarc.npy"
    model_path = "model_kerasarc_v3.h5"
    image_path = "./test_images/"
    plot_path = "./plots/"
    grad_path = "./gradients/arc_test_images_gradients.npy"
    
    # check if model exists, else build
    if not os.path.isfile(model_path):
        build_model(weights_path)
        
    # Explain Face Image Quality at Pixel-Level
    run(image_path, model_path, grad_path, T)
    loaded_gradients = np.load(grad_path, allow_pickle=True)
    plot_comparison(loaded_gradients, plot_path, a, b, True)
    
