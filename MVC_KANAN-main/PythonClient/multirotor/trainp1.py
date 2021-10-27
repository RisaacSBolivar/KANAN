# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:42:11 2021

@author: Karen Benitez
"""

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
# from PIL import ImageGrab
 
path = r'C:\Users\jonat\Documents\GitHub\MVC_KANAN\Reconocimiento_rostros\ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)




face_cascade = cv2.CascadeClassifier(r'C:\Users\jonat\Documents\GitHub\MVC_KANAN\Reconocimiento_rostros\haarcascade_frontalface_default.xml')


for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

            
            
encodeListKnown = findEncodings(images)
print('Encoding Complete')