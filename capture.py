# Importing required modules and library
import numpy as np
from dataPreparation import * 
from PIL import Image
import time
from modelLoader import *
import requests

url = 'http://128.199.176.47:8080/cam_result'
model = modelLoader()
result=[]
def Capture(frame,n):
# Creating the capture object from opencv
    if not os.path.exists('capture_images'):
        print("New directory created")
        os.makedirs('capture_images')
    time.sleep(.3)
    image = frame
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    detections = model.forward()
    # Image from the frame
    ii=0
    for i in range(1):#0, detections.shape[2]):
        box = detections[0,0, i, 3:7] * np.asarray([w,h, w, h])
        (startX, startY, endX, endY) = box.astype('int')
        confidence = detections[0, 0, i, 2]
        if(confidence >= 0.5 and startX>=100 and endX<=600): #and startX>=180 and endX<=420
            br=0
            try:
                if (startY>=50):
                    startY=startY-50
                if (endY+50<=300):
                    endY=endY+50
                frame = image[startY:endY, startX-50:endX+50]
                frame = cv2.resize(frame,(224,224))
                ii=1
                # image_name=f"capture_images/{n}.png"
                cv2.imwrite(f"capture_images/{n}.png",frame)
                # files = {'media': open(image_name, 'rb')}
                # requests.post(url, files=files)
            except:
                print("status=-1 : from capture image file .")
                # url_=url+"?status=-1"
                # x = requests.post(url_, json = {})
                # print("cant capture image",x)
                br=1
            if br==1:
                break

    return ii
