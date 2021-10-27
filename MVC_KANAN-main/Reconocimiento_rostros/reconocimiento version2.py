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
    
    a= False
    b= False
    t1_start = []
    x=0
    while (time.time() - start_time) < 100:  #duración total: 100 segundos
        
        face_cascade = cv2.CascadeClassifier(r'C:\Users\jonat\Documents\GitHub\MVC_KANAN\Reconocimiento_rostros\haarcascade_frontalface_default.xml')
        def markAttendance(name):
            with open(r'C:\Users\jonat\Documents\GitHub\MVC_KANAN\Reconocimiento_rostros\Attendance.csv','r+') as f:
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
                if r==1: 
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-15),(x2,y2),(0,255,0),cv2.FILLED)
                
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                verificacion = True
                
     
            else:
                name="unknown"
                if r==1:
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                verificacion = False       
                

       
        cv2.imshow('Webcam',img) #muestra la ventana de la cámara
        def contador(name,img):
            name=name
            img=img
            val=0
            empezar = time.time()
            while (time.time()-empezar)<2:
              val=0
              
              
              
                
            else:
              val=1
            return val
       
        if verificacion == True: #and rectangulo==1:   #cuando es True, se espera 8 segundos
             
 
            cv2.waitKey(1000) #pausa de 8 segundos y se cierra
            
                            
            #x = contador(name,img)
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


#si r=1 va a aparecer el recuadro y nombre
r=1
nombre, verificacion,lista = reconocimiento(r)
print(nombre, verificacion,lista)
