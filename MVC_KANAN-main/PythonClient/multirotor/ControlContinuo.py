
import setup_path
import airsim
import os
import sys
import math
import time
import argparse
from airsim.types import KinematicsState

import cv2
import time
from time import sleep #Biblioteca para detener la ejecución x segundos
import os
import HandTrackingModule as htm
import sys
import mediapipe as mp

class ControlContinuo:
    def __init__(self):
        """ Conecta con el cliente de Airsim, activa el control mediante API """
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

        self.home = self.client.getMultirotorState().kinematics_estimated.position

    def Despegue(self):
        """ Inicia el despegue del dron """
        self.client.simPrintLogMessage("Bienvenido, Iniciando KANAN",severity=2)
        print("Armando el drone")
        self.client.armDisarm(True)
        self.client.simPrintLogMessage("RETROCEDA POR FAVOR",severity=3)
        time.sleep(5)
        self.client.takeoffAsync().join()
        self.start = self.client.getMultirotorState().kinematics_estimated.position

        #yaw,pitch,roll=airsim.to_eularian_angles(self.client.getMultirotorState().kinematics_estimated.orientation)
        time.sleep(1)


    def movimiento(self):

        cap=cv2.VideoCapture(0)
        detector = htm.handDetector(detectionCon=0.7)
        doIt=True

        x=x2=x3=cont=0 
        step1=step2=step3=False
        step1_1=step2_1=step3_1=False
        gesto1=gesto2=False
        tipIds = [4, 8, 12, 16, 20]
        control = 40

        print("a")
        self.client.moveToPositionAsync(2,2,-10,1,airsim.DrivetrainType.MaxDegreeOfFreedom)
        time.sleep(5)
        print("b")

        while True:
            success, img = cap.read()
            img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
            lmList = detector.findPosition(img, draw=False)

            if doIt==True:
                if len(lmList) != 0:
                    fingers = []

                    #INSTRUCCIONES PARA EL DRON
      				#Controlar dron manualmente
      
      				#Izquierda
                    k=4
    
                    if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]) and (lmList[1][2] < lmList[0][2]) and (lmList[4][1] > lmList[3][1]): #este último es para que el número 4 sea mayor a 3 de izquierda a derecha en la pantalla
                        cv2.putText(img, "Izquierda", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron se mueve a la izquierda")
                        self.client.moveByVelocityAsync(0,-k,0,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()

      				#Dron se mueve hacia arriba
                    if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]) and (lmList[1][2] < lmList[0][2]):
                        cv2.putText(img, "Arriba", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron se nueve hacia arriba")
                        self.client.moveByVelocityAsync(0,0,-k,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()


      				#Dron se mueve hacia la derecha
                    if (control == 40) and (lmList[4][1] < lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                        cv2.putText(img, "Derecha", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron se mueve a la derecha")
                        self.client.moveByVelocityAsync(0,k,0,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()


      				#Dron se mueve hacia abajo
                    if (control == 40) and (lmList[0][2] < lmList[4][2]): #el 2es del eje y
                        cv2.putText(img, "Abajo", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron Abajo")
                        self.client.moveByVelocityAsync(0,0,k,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()

                    #Dron se  mueve hacia adelante: Pulgar y meñique arriba, los demás abajo(Como si estuvieras haciendo un teléfono)
                    if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                        cv2.putText(img, "Adelante", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron se mueve hacia delante")
                        self.client.moveByVelocityAsync(k,0,0,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()

                    #Dron se  mueve hacia atrás, Número 3. Pulgar, índice y medio. 
                    if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
                        cv2.putText(img, "Atras", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        print("Dron se mueve hacia atrás")
                        self.client.moveByVelocityAsync(-k,0,0,0.2,airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False, 0)).join()



                    #Fadul:
      				#FINALIZAR CONTROL MANUAL DEL DRON
      				#Pulgar
                    if (lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]) and (control == 40):
                        fingers.append(1)
                    else:
                        fingers.append(0)
      				#4 dedos
                    for id in range(1,5):
                        if (lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]) and (control == 40):
                            fingers.append(1)
                        else:
                            fingers.append(0)
      
                    totalFingers=fingers.count(1)
      
                    if x2==0 and x3==0 and totalFingers==0 and not gesto1 and (control == 40):
                        if step1_1==False:
                            inicio1=time.time()
                            step1_1=True
                        x=round(time.time()-inicio1,2)
                        if 2>x>1:
                            gesto2=True
                        if x>2:
                            x=x2=x3=0
                            step1_1=False
                        cv2.putText(img, str(x)+" iniciando gesto 2" , (250,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
      				###
                    if gesto2:
                        if(totalFingers==5):
                            if step2_1==False:
                                inicio2=time.time()
                                step2_1=True
                            x2=round(time.time()-inicio2,2)
                            if x>2:
                                x=x2=x3=0
                                step2_1=False
                            cv2.putText(img,str(x2) , (450,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
      					
                        if 2>x2>1 and totalFingers==0:
                            if step3_1==False:
                                inicio3=time.time()
                                step3_1=True
                            x3=round(time.time()-inicio3,2)
                            if x>2:
                                x=x2=x3=0
                                step2_1=False
                            cv2.putText(img, str(x3), (450,60), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                        if 1.7>x3>1.5:
                            doIt=False
                            cont=200
      					####
                    if totalFingers !=5:
                        step1=False
                        step3=False
                        step2_1=False
                    if totalFingers !=0:
                        step2=False
                        step1_1=False
                        step3_1=False

      		#Fadul:
      		#Aqui se finaliza el contro manual
            if cont>0:
                cont=cont-1
                if gesto2:
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return "Termina control"
                if cont==1:
                    doIt=True
                    x=x2=x3=0
                    gesto1=gesto2=False
      
            cv2.imshow("Image", img)
            cv2.waitKey(1)
      
            img = detector.findHands(img) #Esto nos muestra la mano. La detecta
            lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList.
      
            if cv2.waitKey(1) == 27: #De esta forma podemos salir del bucle. Es 27 haciendo referencia  a la tecla scape.
                cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                cap.release();
                break

    def Aterrizaje(self):
        """ Desactiva el control de API y desarma el dron """
        #self.client.moveToPositionAsync(self.start.x_val,self.start.y_val,self.start.z_val,5).join
        self.client.simPrintLogMessage("...Aterrizando...",severity=1)
        self.client.hoverAsync().join()
        self.client.landAsync().join()
        self.client.simPrintLogMessage("...Desarmando...",severity=0)
        self.client.armDisarm(False)
        self.client.enableApiControl(False)




if __name__ == "__main__":
    mov = ControlContinuo()
    mov.Despegue()
    mov.movimiento()

