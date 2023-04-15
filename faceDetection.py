import cv2
import typing
import numpy as np
import mediapipe as mp
import os
import time

mp_drawing_utils = True
color = (255, 255, 255)
confidence=0.5
thickness = 2
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=confidence)

def tlbr( frame: np.ndarray, mp_detections: typing.List) -> np.ndarray:
    detections = []
    frame_height, frame_width, _ = frame.shape
    for detection in mp_detections:
        height = int(detection.location_data.relative_bounding_box.height * frame_height)
        width = int(detection.location_data.relative_bounding_box.width * frame_width)
        left = max(0 ,int(detection.location_data.relative_bounding_box.xmin * frame_width))
        top = max(0 ,int(detection.location_data.relative_bounding_box.ymin * frame_height))
        if left >=100 and (left + width)<=600:
            #print(f"top {top}, left {left}, bottom {top + height},right {left + width} ")
            detections.append([top, left, top + height, left + width])
    return np.array(detections)

def detection( frame: np.ndarray, return_tlbr: bool = False) -> np.ndarray:
    """Main function to do face detection"""
    detect=0
    results = face_detection.process(frame)
    if results.detections:
        i=0
        for tlbr_ in tlbr(frame, results.detections):
            if i==0:
                detect=1
                cv2.line(frame, (100,0), (100,800), (color),  thickness)
                cv2.line(frame, (600,0), (600,800), (color),  thickness)
                cv2.rectangle(frame, tlbr_[:2][::-1], tlbr_[2:][::-1], color, thickness)
                i=+1
            else:
                detect=0
    return  frame,detect