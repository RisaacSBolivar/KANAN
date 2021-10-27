############################################
################### KANAN ##################
############################################

from pprint import pprint
from airsim import client

from airsim.types import KinematicsState

import setup_path
import airsim
import orbit 
import os

import sys
import math
import time 
import argparse
import numpy

import GestosConTiempo as gt
import pruebafinal as dp

import numpy as np
#import pruebafinal as pf
import cv2

import ControlContinuo
import pruebatrackf_f as tk

import telebot_Kanan as tbk

import yolov as y3
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------







class KANAN:
    def __init__(self):
        """ Conecta con el cliente de Airsim, activa el control mediante API """
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

        self.Autorizacion = False #Autorizacion de vuelo
        self.Registro_de_vuelo = [] #Registro
        self.piloto = ""
        self.Resgistro_de_Objetos= []
    
    def Despegue(self):
        """ Inicia el despegue del dron """
        self.client.simPrintLogMessage("Bienvenido, Iniciando KANAN",severity=2)
        tbk.enviar_mensaje("Bienvenido, Iniciando KANAN","chatG")
        print("Armando el drone")
        self.client.armDisarm(True)
        self.client.simPrintLogMessage("RETROCEDA POR FAVOR",severity=3)
        tbk.enviar_mensaje("RETROCEDA POR FAVOR","chatG")
        time.sleep(5)
        self.client.takeoffAsync().join()
        self.start = self.client.getMultirotorState().kinematics_estimated.position

        #yaw,pitch,roll=airsim.to_eularian_angles(self.client.getMultirotorState().kinematics_estimated.orientation)
        time.sleep(1)
        
        
    def Escaneo_Entorno(self):
        """ Rota el dron 360° y obtiene informacion de lidar """
        self.client.simPrintLogMessage("Escaneo de entorno",severity=2)
        self.client.rotateByYawRateAsync(45,8)

        for i in range(1,5):
            lidarData = self.client.getLidarData();
            if (len(lidarData.point_cloud) < 3):
                print("\tNo hay puntos")
            else:
                points = self.parse_lidarData(lidarData)
                print("\Lectura %d: tiempo: %d Numero de puntos: %d" % (i, lidarData.time_stamp, len(points)))
                print(points[0:20])
    
            time.sleep(2)

    def yoloFoto(self):
        responses = self.client.simGetImages([airsim.ImageRequest("low_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
        response = responses[0]
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
        img_rgb = img1d.reshape(response.height, response.width, 3)        
        #tiempoLimite = 10
        #print(y3.deteccionUnica(img_rgb))
        tbk.enviar_mensaje(str(y3.deteccionUnica(img_rgb)) + " " + str(self.client.getMultirotorState().kinematics_estimated.position),self.piloto)

    def parse_lidarData(self, data):

        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def Verificacion_ID(self):
        """ Verifica y registra la identidad del piloto """
        self.client.simPrintLogMessage("INICIANDO COMPROBACION DE IDENTIDAD",severity=2)
        tbk.enviar_mensaje("INICIANDO COMPROBACION DE IDENTIDAD","chatG")
        import reconocimiento_version3 as fr
        name,self.Autorizacion,lista_reconocimiento = fr.reconocimiento(1)

        if self.Autorizacion:
            if len(self.Registro_de_vuelo)==0:
                self.Registro_de_vuelo.append(name)
            
            if not name in self.Registro_de_vuelo:
                self.Registro_de_vuelo.append(name)
            
            self.piloto = name
            self.client.simPrintLogMessage("El piloto es: ", self.piloto,severity=2)
            tbk.enviar_mensaje("El piloto es: "+ self.piloto,"chatG")

    def Aterrizaje(self):
        """ Desactiva el control de API y desarma el dron """
        #self.client.moveToPositionAsync(self.start.x_val,self.start.y_val,self.start.z_val,5).join
        self.client.simPrintLogMessage("...Aterrizando...",severity=1)
        self.client.hoverAsync().join()
        self.client.landAsync().join()
        self.client.simPrintLogMessage("...Desarmando...",severity=0)
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
        tbk.enviar_mensaje("Gracias por volar con KANAN","chatG")

    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------


    def Rutina_1_Video(self):
        self.client.simPrintLogMessage("Iniciando Rutina 1",severity=1)

        out = cv2.VideoWriter('outputFinal3.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 20, (1920,1080))
        time.sleep(5)
        self.client.moveToPositionAsync(2,0,-4,1,airsim.DrivetrainType.MaxDegreeOfFreedom).join()
        time.sleep(2)
        self.client.rotateToYawAsync(-180).join()
        time.sleep(5)
        self.client.moveByVelocityAsync(0.5,0,-0.5,20,airsim.DrivetrainType.MaxDegreeOfFreedom)
        #self.client.rotateByYawRateAsync(10, 30)

        tbk.enviar_mensaje("Iniciando grabación",self.piloto)
        contador = 0
        while contador != 100:
            responses = self.client.simGetImages([airsim.ImageRequest("high_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
            img_rgb = img1d.reshape(response.height, response.width, 3) 
            out.write(img_rgb)
            contador = contador + 1

        out.release()
        time.sleep(4)
        tbk.enviar_video('outputFinal3.mp4', self.piloto)

        self.client.moveToPositionAsync(0, 0, -5, 10).join()
        self.client.hoverAsync().join()
    
    def Rutina_2_Circulo(self):
        
        self.client.simPrintLogMessage("Iniciando Rutina 2",severity=1)
        self.client.simPrintLogMessage("Seleccione el numero de fotos a tomar",severity=2)
        #numero = dp.gestosEstaticos()
        #print(numero)
        #numF = numero + 2
        mensaje = "Se tomaran 2 fotos"
        tbk.enviar_mensaje(mensaje,self.piloto)
        nav = orbit.OrbitNavigator(4, 6, 2, 1, [1,0], 2)
        nav.start()
        time.sleep(4)
        self.client.moveToPositionAsync(0, 0, -5, 1).join()
        tbk.enviar_foto("photo_1.png",self.piloto)

    def Rutina_3_Reconocimiento(self):
        self.client.simPrintLogMessage("Iniciando Reconocimiento de objetos",severity=2)
        tbk.enviar_mensaje("Iniciando reconocimiento de Objetos",self.piloto)
        
        z=-6
        self.client.moveOnPathAsync([airsim.Vector3r(0,0,z),airsim.Vector3r(125,0,z),
                                    airsim.Vector3r(125,125,z),
                                    airsim.Vector3r(0,125,z),
                                    airsim.Vector3r(-125,125,z),
                                    airsim.Vector3r(-125,-5,z)],
                                    5,140,
                                    airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False,0),7.5,1)


        out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1920,1080))
        contador = 0
        while contador != 300:
            responses = self.client.simGetImages([airsim.ImageRequest("high_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
            img_rgb = img1d.reshape(response.height, response.width, 3) 
            out.write(img_rgb)
            contador = contador + 1


        out.release()

        # = 0
        #while contador != 20:
        #    self.yoloFoto()
        #    time.sleep(5)
        #    contador = contador + 1
        #self.client.hoverAsync().join()
        #self.client.moveToPositionAsync(0, 0, -5, 10).join()

    def Rutina_4_Tracking(self):
        self.client.simPrintLogMessage("Iniciando Tracking",severity=3)
        track = tk.Tracking()
        track.deteccionContinua("car")


    def Rutina_5_Control(self):
        self.client.simPrintLogMessage("Iniciando Control Continuo",severity=3)
        tbk.enviar_mensaje("Iniciando Control Continuo",self.piloto)
        mov = ControlContinuo.ControlContinuo()
        mov.movimiento()
        self.client.moveToPositionAsync(0, 0, -5, 15).join()



        

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    sim = KANAN()

    sim.Despegue()

    estado_de_V = True
    entornoV = True
    while estado_de_V:
        sim.Verificacion_ID()
        if not sim.Autorizacion:
            break
        if entornoV == False:
            sim.Escaneo_Entorno()
            entornoV = True

        atencion = gt.gestosMov()

        if atencion == False:
            estado_de_V =False
            

        while atencion == True:

            accion = dp.gestosEstaticos()

            if accion == 1: 
                print("Video")
                atencion = False
                sim.Rutina_1_Video()

            if accion == 2: 
                print("Circulo")
                sim.Rutina_2_Circulo()
                atencion = False

            if accion == 3: 
                print("Reconocimiento")
                sim.Rutina_3_Reconocimiento()
                atencion = False
            
            if accion == 4:
                print("Tracking")
                sim.Rutina_4_Tracking()
                atencion = False

            if accion == "Control":
                print("Control")
                sim.Rutina_5_Control()
                atencion = False

            if accion == "Churros":
                print("Salida")
                estado_de_V =False
                break

    if sim.Autorizacion == False:
        sim.client.simPrintLogMessage("USUARIO NO AUTORIZADO",severity=3)
        tbk.enviar_mensaje("Un usuario no autorizado esta intentando volar","chatG")

    else:
        sim.client.simPrintLogMessage("Gracias por volar con KANAN!",severity=2)
        print(sim.Registro_de_vuelo)
        
    sim.Aterrizaje()
    tbk.enviar_mensaje("Pilotos: " + str(sim.Registro_de_vuelo),"chatG")

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
# SIAFI UNAM 2021
# Autores:
# Ándres Fábian Pérez Suaréz
# Angel Josafat Vázquez Minor
# Jesús Martínez Fadul
# Jeremy Dimitri Larios Hernández
# Jonathan Yair Vazquez Uriostegui
# Karen Lizeth Benítez Fuentes
# Leonardo Nicolás Hernández

  
   
