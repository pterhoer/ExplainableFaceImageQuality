# Preprocessing of Images

# This script provides image the preprocessing function using MTCNN 
# Parts of this file are strongly adapted from:
# https://github.com/deepinsight/insightface/blob/master/src/common/face_preprocess.py   

# Author: Marco Huber, 2020
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de


import cv2
import numpy as np

from mtcnn import MTCNN
from skimage import transform

def setup_img(img):
    """
    Prepares the input image

    Parameters
    ----------
    img : img array
        The preprocessed and aligned keras model.

    Returns
    -------
    in_img : TYPE
        Prepared image ready to be fed into the network.

    """    
    
    # preprare image
    in_img = preprocess_img(img)
    
    if in_img is None:
        return None
        
    in_img = np.expand_dims(in_img, axis=0)
    in_img = np.moveaxis(in_img, 1, 3)
    
    return in_img
    
def preprocess_img(img):
    """
    Aligns and preprocess the provided image

    Parameters
    ----------
    img : array of the images
        The image to be aligned and preprocessed.

    Returns
    -------
    nimg : numpy ndarray
        Aligned and processed image.

    """
    # define thresholds
    thrs = [0.6,0.7,0.8]
    
    # get detector
    detector = MTCNN(steps_threshold=thrs)
    
    # detect face
    detected = detector.detect_faces(img)
    
    if detected is None or detected == []:
        print("MTCNN could not detected a face.")
        return None

    # get box and points
    bbox, points = detected[0]['box'], detected[0]['keypoints']

    # rearrange points
    p_points = []
    for v in points.values():
        p_points.append(v)
        
    p_points = np.asarray(p_points)

    # preprocess
    nimg = preprocess(img, bbox, p_points, image_size="112,112")
    nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
        
    return np.transpose(nimg, (2,0,1))


def read_image(img_path, **kwargs):
  
    mode = kwargs.get('mode', 'rgb')
    layout = kwargs.get('layout', 'HWC')
  
    if mode=='gray':
        img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    else:
        img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_COLOR)
        if mode=='rgb':
            img = img[...,::-1]
        if layout=='CHW':
            img = np.transpose(img, (2,0,1))
    return img

def preprocess(img, bbox=None, landmark=None, **kwargs):
  
    if isinstance(img, str):
        img = read_image(img, **kwargs)
  
    M = None
    image_size = []
    str_image_size = kwargs.get('image_size', '')
  
    if len(str_image_size)>0:
        image_size = [int(x) for x in str_image_size.split(',')]
        if len(image_size)==1:
            image_size = [image_size[0], image_size[0]]
        assert len(image_size)==2
        assert image_size[0]==112 or image_size[0]==160
        assert image_size[0]==112 or image_size[1]==96 or image_size[0]==160
    
    if landmark is not None:
        assert len(image_size)==2
        src = np.array([
            [30.2946, 51.6963],
            [65.5318, 51.5014],
            [48.0252, 71.7366],
            [33.5493, 92.3655],
            [62.7299, 92.2041] ], dtype=np.float32)
        if image_size[1]==112 or image_size[1]==160:
            src[:,0] += 8.0
        dst = landmark.astype(np.float32)

        tform = transform.SimilarityTransform()
        tform.estimate(dst, src)
        M = tform.params[0:2,:]

    if M is None:
        if bbox is None: 
            det = np.zeros(4, dtype=np.int32)
            det[0] = int(img.shape[1]*0.0625)
            det[1] = int(img.shape[0]*0.0625)
            det[2] = img.shape[1] - det[0]
            det[3] = img.shape[0] - det[1]
        else:
            det = bbox
        margin = kwargs.get('margin', 44)
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img.shape[1])
        bb[3] = np.minimum(det[3]+margin/2, img.shape[0])
        ret = img[bb[1]:bb[3],bb[0]:bb[2],:]
        if len(image_size)>0:
            ret = cv2.resize(ret, (image_size[1], image_size[0]))
        return ret 
    else: 
        assert len(image_size)==2
        warped = cv2.warpAffine(img,M,(image_size[1],image_size[0]), borderValue = 0.0)
        return warped

