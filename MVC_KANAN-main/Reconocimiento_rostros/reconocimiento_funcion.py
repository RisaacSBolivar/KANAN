# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:19:17 2021

@author: Karen Benitez
"""

from datetime import datetime, timedelta
import cv2
import numpy as np
import face_recognition
import os
from trainp1 import encodeListKnown
from trainp1 import classNames
import time 
from time import perf_counter



def reconocimiento():
    start_time = time.time()
    verificacion = False
    name = " "
    lista_reconocimiento = []
    end_time = datetime.now() + timedelta(seconds=40)
    cap = cv2.VideoCapture(0)
    
    a= False
    b= False
    t1_start = []


    
    while (time.time() - start_time) < 100:
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        def markAttendance(name):
            with open('Attendance.csv','r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'n{name},{dtString}')
        
        
        #success, img = cap.read()
        img = cv2.imread("7.png")
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
             
        gray = cv2.cvtColor (imgS,cv2.COLOR_BGR2GRAY) 
        faces_c = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
              
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
                 
        for (x,y,w,h) in faces_c:
                
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            color = (255,0,0)
            stroke = 2
            width = x + w
            height = y + h
            cv2.rectangle(imgS, (x,y), (width,height),color,stroke)
                
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
           
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                    
            matchIndex = np.argmin(faceDis)
            
                 
            if matches[matchIndex]:
                time_v2 = time.time()
                name = classNames[matchIndex].upper()
                  
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-15),(x2,y2),(0,255,0),cv2.FILLED)
            
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                verificacion = True
                
     
            else:
                name="unknown"
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                verificacion = False       
                
        
        
         
       
                
        
         

       
        cv2.imshow('Webcam',img)
        if (time.time()-start_time)>8 and verificacion == True :
            startt = time.time()
            time.sleep(5)
            if (time.time()-startt >5):
                
                img_name = "person" +".png"
                cv2.imwrite(str(img_name),img)
                a=True
                break
            if a == True:
                b=True
                break
        if b==True:

            break
                        
                 
        
        
        if cv2.waitKey(20) & 0xFF ==ord('q'):
            break
       
    cap.release()
    cv2.destroyAllWindows()
    
    lista_reconocimiento.append(name) #se anexa nombre
    lista_reconocimiento.append(verificacion) #se anexa verificación
    
    return name, verificacion,lista_reconocimiento
        

nombre, verificacion,lista = reconocimiento()
print(nombre, verificacion,lista)

