import numpy as np
import cv2
import os
import cvlib as cv
# from runGEARP import * 
import requests
url_img = 'http://128.199.176.47:2023/api/face'
result_age=[]
result_gender=[]
classes = ['male','female']
gender_result = []
def send_image():
    # Loop through all images and save images with marked faces
    for file in os.listdir('capture_images'):
        file_name, file_extension = os.path.splitext(file)
        
        if (file_extension in ['.png','.jpg','.jpg','.jpeg']):
            #print("Image path: {}".format('capture_images/' + file))
            im1  = 'capture_images/'  + file
            with open(im1, "rb") as image_file:
                # create the request data as a dictionary
                data = {"image": ("image.jpg", image_file, "image/jpeg")}

                # send the request using the requests library
                response = requests.post(url_img, files=data)
            if (len(response.json())>0):
                print(file)
                result_age.append(response.json()[0]["age"])
                result_gender.append(response.json()[0]["gender"])
            os.remove(im1)
# send_image()