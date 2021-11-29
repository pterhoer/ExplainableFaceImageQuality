# Implementation of SER-FIQ based on Keras

# Author: Marco Huber, 2020
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de

import numpy as np

from tensorflow.keras import backend as K
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances

from auxiliary_models import get_pre_dropout_state, get_stochastic_pass_model

def get_scaled_quality(img, model, T, alpha, r):
    """
    Returns the scaled SER-FIQ quality of an image
    
    Performs Unsupervised Estimation of Face Image Quality Based on Stochastic
    Embedding Robustness (SER-FIQ) based on the arcface keras model.
    
    SEF-FIQ was proposed by Terhörst, Kolf, Damer, Kirchbuchner and 
    Kuijper at CVPR, 2020
    
    Parameters
    ----------
    img : preprocess and aligned image
        The image to be processed.
    model : Keras model
        The model to be used.
    T : int
        number of stochastic forward passes.
    alpha : float
        Scaling parameter.
    r : float
        Scaling parameter.
    
    Returns
    -------
    Robustness score: float64
        The scaled SER-FIQ score.

    """
    
    # get pre-dropout state
    state = get_pre_dropout_state(img, model)
    
    # get stochastic part
    stochastic_model = get_stochastic_pass_model(model)
   
    # repeat T times
    t_states = np.repeat(state, repeats=T, axis=0)
    
    # predict
    X = stochastic_model.predict(t_states)
  
    # normalize
    norm = normalize(X, axis=1)
    
    # calculate SER_FIQ quality
    eucl_dist = euclidean_distances(norm, norm)[np.triu_indices(T, k=1)]
    quality = 2*(1/(1+np.exp(np.mean(eucl_dist)))) 
    
    # scale
    quality = 1 / (1+np.exp(-(alpha * (quality - r))))
  
    # clear model
    del stochastic_model
    K.clear_session() 
    
    return quality
