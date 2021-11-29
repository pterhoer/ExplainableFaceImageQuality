# File to calculate the gradients

# Author: Marco Huber, 2021
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de

import numpy as np
import tensorflow as tf

from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import BatchNormalization, Dense, Flatten, Lambda

def euclid_normalize(x):
    return K.l2_normalize(x, axis=1)

def calculate_weights(quality, emb):
    
     # calculate weights
     sum_act = np.sum(emb)
     w = quality / sum_act
     
     # build array
     arr_w = np.repeat(w, len(emb))
     arr_w = arr_w.reshape((1, len(emb), 1))
     return arr_w

def get_gradients(image, model, quality):
    
    # build model
    curr_out = model.get_layer('bn1').output
    x = Flatten(name="flatten")(curr_out)  
    x = Dense(name='pre_fc1', units=512, use_bias=True)(x)
    x = BatchNormalization(name='fc1', axis=1, epsilon=1.9999999494757503e-05, center = True, scale = False)(x)
    embedding = Lambda(euclid_normalize, name="euclidnorm")(x)
       
    # expand model with quality part
    out = Dense(1, activation="linear", use_bias=False, name="quality")(embedding)
    
    # define model
    grad_model = Model(model.inputs, [out, embedding])
    
    # set weights
    grad_model.get_layer('pre_fc1').set_weights(model.get_layer('pre_fc1').get_weights())
    
    # get current embedding to adjust quality weights
    _, curr_emb = grad_model.predict(image)
    curr_emb = curr_emb.squeeze()
    
    # set quality weights
    grad_model.get_layer('quality').set_weights(calculate_weights(quality, curr_emb))
   
    # calculate gradients
    with tf.GradientTape() as gtape:
        inputs = tf.cast(image, tf.float32)
        gtape.watch(inputs)
        outputs, _ = grad_model(inputs)

    # get gradients
    grads = gtape.gradient(outputs, inputs)[0]
    
    # clear model
    del grad_model
    K.clear_session() 
    
    return grads