# main.py
from faceDetection import detection#,capture
from hand_gesture_v1 import gesture_detect_v1
from send_image import *
import cv2 as cv
import time
from runGEARP import *
import requests
import numpy as np
import statistics as stat
url = 'http://128.199.176.47:8080/cam_result'
url_img = 'http://128.199.176.47:2023/api/face'

#Creating the object for GEAR predictor
obj = GEARP()
webcam_id= 0
def close_vid(frame):
    cv.imshow('Window', frame)
    # time.sleep(1)

def process_result():
    if len(result_age)>0:
        age_summation=0
        count_age=0
        age_avg=0
        min_distance=5
        male=0
        female=0
        res=()
        
        age_median=stat.median(result_age)
        print("median : ",age_median)
        for i in range (len(result_age)):
            tracker=0
            if age_median>=result_age[i]:
                if (age_median-result_age[i])<=min_distance :
                    age_summation=age_summation+result_age[i];
                    count_age=count_age+1
                    tracker=1
            elif age_median<=result_age[i]:
                    if (result_age[i]-age_median)<=min_distance :
                        age_summation=age_summation+result_age[i];
                        count_age=count_age+1
                        tracker=1
            if tracker==1:
                if result_gender[i]=="male":  # gender
                    male+=1
                elif result_gender[i]=="female":
                    female+=1
            tracker=0
        age_avg = (age_summation/count_age)
        age_avg=age_avg//1 +1
        print("age sum : ",age_summation," age average: ",age_avg," taken image: ",count_age," male numb: ",male)
        
        gender=[male,female]
        gender_name=["male","female"]
        
        gender_ = np.array(gender)
        gender_index = np.argmax(gender_)
        age_s=f"[{age_avg-3} - {age_avg+3}]"
        res=(age_s,gender_name[gender_index])
        myobj = {'result': res}
        print("my object : ",myobj)
        url_=url+"?status=3"
        x = requests.post(url_, json = myobj)
        

def face_detect():
    frame_rate = 100
    prev = 0
    face_detect=0
    cap_image=10
    no_captur=0
    n=0
    captur=0
    start_time=0#time.time()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        url_=url+"?status=0"
        x = requests.post(url_, json = {})
        print("not video open ",x)
    
    # print("cap open ",cap.isOpened())
    while cap.isOpened():  
        time_elapsed = time.time() - prev
        success, frame = cap.read()
        if not success:
            url_=url+"?status=0"
            x = requests.post(url_, json = {})
            print("not video open ",x)
            break
        else:
            frame=cv.flip(frame,1)
            if time_elapsed > 1./frame_rate:
                prev = time.time()
                if not success or frame is None:
                    print("Ignoring empty camera frame.")
                    continue
                if face_detect==0:
                    frame,face_det =  detection(frame)
                    cv.putText(img=frame, text="Please come in the middle ", org=(50, 50), 
                    fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,0),thickness=2)
                    if face_det:
                        url_=url+"?status=1"
                        x = requests.post(url_, json = {})
                        print("face detected ",x)
                        face_detect=1
                        start_time=time.time()
                elif face_detect==1:
                    # frame,hand =gesture_detect(frame,hands,keypoint_classifier,keypoint_classifier_labels)
                    frame,hand=gesture_detect_v1(frame)
                    cv.putText(img=frame, text="Show victory sign in "+str((time.time()-start_time))+" second", org=(50, 50), 
                        fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,255),thickness=2)
                    if not hand and ((time.time()-start_time))>=10:
                        url_=url+"?status=-1"
                        x = requests.post(url_, json = {})
                        print("time out waiting for gesture",x)
                        break
                    if hand:
                        url_=url+"?status=2"
                        x = requests.post(url_, json = {})
                        print("hand sign detected ",x)
                        start_time=time.time()
                        face_detect=2
                elif face_detect==2:
                        if no_captur<10:
                            captur = obj.Capture(frame,no_captur)
                        cv.putText(img=frame, text="Capturing image, "+str((time.time()-start_time))+" seconds", org=(0, 50), 
                        fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(255,255,255),thickness=2)
                        no_captur+=captur
                        captur=0
                        if  no_captur<=0 and ((time.time()-start_time))>=4:
                            url_=url+"?status=-1"
                            x = requests.post(url_, json = {})
                            print("time out waiting for capture",x)
                            break
                        if (time.time()-start_time)>=4:
                            break
            close_vid(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv.destroyAllWindows()
    cap.release()

def main():
                   #face detection
    if (True):
        # Create a VideoCapture object for given webcam_id
        print("WEB OPENING")
        face_detect()
        send_image()
        if len(result_age)>0:
            print(result_age)
            process_result()
        else:       #if age gender not detect
            url_=url+"?status=-1"
            x = requests.post(url_, json = {})
            print("can't detected",x)
main()