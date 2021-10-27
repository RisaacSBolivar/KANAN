############################################
################### KANAN ##################
############################################
from pprint import pprint

from airsim.types import KinematicsState

import setup_path
import airsim

import os

import sys
import math
import time 
import argparse
import numpy

import GestosConTiempo as gt
import GestosEst as dp

import yolov2 as y3



class KANAN:
    def __init__(self):
        
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

       



        
    
    def Despegue(self):
        print("Armando el drone")
        self.client.armDisarm(True)
        self.client.simPrintLogMessage("RETROCEDA POR FAVOR",severity=3)
        time.sleep(5)
        self.client.takeoffAsync().join()
        self.start = self.client.getMultirotorState().kinematics_estimated.position

        yaw,pitch,roll=airsim.to_eularian_angles(self.client.getMultirotorState().kinematics_estimated.orientation)
        
        

    
        
    def Escaneo_Entorno(self):
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

    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def Verificacion_ID(self):
        self.client.simPrintLogMessage("INICIANDO COMPROBACION DE IDENTIDAD",severity=2)
        
    def Rutina_1(self):
        self.client.simPrintLogMessage("Iniciando Rutina 1",severity=1)
        time.sleep(1)
        self.client.moveToPositionAsync(2,0,-4,1,airsim.DrivetrainType.MaxDegreeOfFreedom).join()
        time.sleep(2)
        self.client.rotateToYawAsync(-180).join()
        time.sleep(5)
        self.client.moveByVelocityAsync(2,0,-2,16).join()
        time.sleep(5)
        self.client.moveToPositionAsync(self.start.x_val,self.start.y_val,self.start.z_val,4,airsim.DrivetrainType.ForwardOnly).join()
        

        
        




    def Rutina_2(self):
        self.client.simPrintLogMessage("Iniciando Rutina 2",severity=1)
        time.sleep(5)
        z=-20
        self.client.moveOnPathAsync([airsim.Vector3r(130,0,z),
                                    airsim.Vector3r(130,20,z),
                                    airsim.Vector3r(0,20,z),
                                    airsim.Vector3r(0,40,z),
                                    airsim.Vector3r(130,40,z)],
                                    6,73,
                                    airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False,0),9,1)
        
        time.sleep(20)
        responses = self.client.simGetImages([airsim.ImageRequest("high_res", airsim.ImageType.Scene)]) #scene vision image in png format
        response = responses[0]
        filename = "photo_1" 
        #self.snapshot_index += 1
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)        
        print("Saved snapshot: {}".format(filename))
        time.sleep(45)
        responses = self.client.simGetImages([airsim.ImageRequest("low_res", airsim.ImageType.Scene)]) #scene vision image in png format
        response = responses[0]
        filename = "photo_2" 
        #self.snapshot_index += 1
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)        
        print("Saved snapshot: {}".format(filename))
        self.client.moveToPositionAsync(self.start.x_val,self.start.y_val,self.start.z_val,5).join()
        
        
                                

        

        



    def Aterrizaje(self):
        #self.client.moveToPositionAsync(self.start.x_val,self.start.y_val,self.start.z_val,5).join
        self.client.simPrintLogMessage("Aterrizando...",severity=1)
        self.client.hoverAsync().join()
        self.client.landAsync().join()
        self.client.simPrintLogMessage("Desarmando...",severity=0)
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
        


    
        


if __name__ == "__main__":

    sim = KANAN()
    sim.Despegue()
    sim.Escaneo_Entorno()
    sim.Aterrizaje()

  
   



   


 



