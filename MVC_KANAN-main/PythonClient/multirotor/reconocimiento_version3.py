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



def reconocimiento(r):
    
    start_time = time.time()
    verificacion = False
    name = " "
    lista_reconocimiento = []
    end_time = datetime.now() + timedelta(seconds=40)
    cap = cv2.VideoCapture(0)
    no_es = 0
    si_es= 0
    contador = 0
    a= False
    b= False
    t1_start = []
    x=0
    while (time.time() - start_time) < 100:  #duración total: 100 segundos
        
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
        
        
        success, img = cap.read()
       
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
            
                 
            if matches[matchIndex]:    #si sí reconoce
                time_v2 = time.time()
                name = classNames[matchIndex].upper()
                verificacion = True
                markAttendance(name)
                
                si_es = si_es+1
                contador = si_es  
				
                si_es = contador 
                contador = 0
                
                if r==1: 
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(231,130,35),5)
                    cv2.rectangle(img,(x1,y2-15),(x2,y2),(231,130,25),cv2.FILLED)
                
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,2,(52,164,204),2)
                
                
     
            else:
                name="unknown"
                markAttendance(name)
                verificacion = False 
                markAttendance(name)
                no_es = no_es+1 
                contador = no_es
				
                no_es = contador  
				
                
                contador = 0
                if r==1:
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
                     
                

       
        cv2.imshow('Webcam',img) #muestra la ventana de la cámara
        
       
        if (si_es>20) and verificacion == True: #and rectangulo==1:   #cuando es True, se espera 8 segundos
             
            
            #cv2.waitKey(8000) #pausa de 8 segundos y se cierra
           
            x=1

            
        if x==1:
            
            break

        
        
        
                        
                 
        
        
        if cv2.waitKey(20) & 0xFF ==ord('q'):  #presiona 'q' para salir en cualquier momento
            break
       
    cap.release()
    cv2.destroyAllWindows()
    
    lista_reconocimiento.append(name) #se anexa nombre
    lista_reconocimiento.append(verificacion) #se anexa verificación
    
    return name, verificacion,lista_reconocimiento

