# Auxiliary Models for Explainable Face Image Quality

# This script contains auxiliary functions for the models.

# Author: Marco Huber, 2020
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de


from tensorflow.keras import backend as K
from tensorflow.keras import Model
from tensorflow.keras.layers import (Input, Dense, BatchNormalization, 
                                Dropout, Lambda)

from kerasarc_v3 import KitModel, load_weights_from_file

def euclid_normalize(x):
    return K.l2_normalize(x, axis=1)

def build_model(weights_path):
    
    model = KitModel(weights_path)
    model.save("model_kerasarc_v3.h5")

def get_pre_dropout_state(img, model):
    """
    Returns the pre-dropout layer activations

    Parameters
    ----------
    img : numpy ndarray
        The alinged, preprocessed and batch-ified image
    model : keras model
        The used model

    Returns
    -------
    state : numpy array
        The activation state before the stochastic dropout layer.

    """
    # define new model
    pre_dropout_model = Model(inputs=model.input, outputs=model.get_layer('flatten').output)
    
    # calculate state
    state = pre_dropout_model(img)
    
    # delete model
    del pre_dropout_model
    
    return state


def get_stochastic_pass_model(model):
    """
    Returns a minimized model only consisting of the stochastic model part

    Parameters
    ----------
    model : keras model
        The model to be used for the stochastic forward pass.
 
    Returns
    -------
    stochastic_pass_model : keras model
        Minimized keras model only including the stochastic part of the model.

    """
    
    # define stochastic model
    inputs = Input(shape=(25088,))
    x = inputs
    
    x = Dropout(name='dropout', rate=0.5)(x, training=True)
    x = Dense(name='pre_fc1', units=512, use_bias=True)(x)
    x = BatchNormalization(name='fc1', axis=1, epsilon=1.9999999494757503e-05, center = True, scale = False)(x)
    x = Lambda(euclid_normalize)(x)
    output = x
    
    # declare model
    stochastic_pass_model = Model(inputs=inputs, outputs=output)
    stochastic_pass_model.get_layer('pre_fc1').set_weights(model.get_layer('pre_fc1').get_weights())
    
    return stochastic_pass_model

    