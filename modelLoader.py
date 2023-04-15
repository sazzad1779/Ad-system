from keras.models import load_model
import cv2
import os

def modelLoader():
    
    # Define paths
    prototxt_path = 'trainedModels/deploy.prototxt'
    caffemodel_path = 'trainedModels/weights.caffemodel'

    # Read the model for opencv
    model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

    return ( model)