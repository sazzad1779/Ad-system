
import cv2
import numpy as np
import mediapipe as mp
# import logging
# logging.getLogger('tensorflow').disabled = True
import tensorflow as tf
from tensorflow.keras.models import load_model


# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# Load the gesture recognizer model
model = tf.keras.models.load_model('trainedModels/Hand_Gesture_Model.h5') # Loading the H5 Saved Model
# Load class names
f = open('trainedModels/gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
def gesture_detect_v1(frame):
    x, y, c = frame.shape
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    hand=0
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            prediction = model.predict([landmarks],verbose = 0)
            # print(prediction)
            
            classID = np.argmax(prediction)
            if classID==1:
                className = classNames[classID]
                print(f"getting {className} sign.")
                hand=1
    return frame,hand