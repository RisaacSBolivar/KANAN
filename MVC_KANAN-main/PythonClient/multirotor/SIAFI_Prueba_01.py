############################################
################### KANAN ##################
############################################


import setup_path
import airsim

import sys
import math
import time 
import argparse
import numpy as np

import GestosConTiempo as gt
import GestosEst as dp

import orbit 

import yolov as y3

def yoloFoto():
    responses = client.simGetImages([airsim.ImageRequest("high_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)        
    tiempoLimite = 10
    print(y3.deteccionUnica(img_rgb))


client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
entrada = 0

print("Armando el drone")
client.armDisarm(True)
time.sleep(1)
client.takeoffAsync().join()



duration = 5
speed = 4
z = -10

#Karen y Angel
#import reconocimiento_version3 as fr
#name,verificar,lista_reconocimiento = fr.reconocimiento(1)
verificar=True

if verificar == True:
    entrada1 = gt.gestosMov()

    while entrada1 == True:
        
        entrada = dp.gestosEstaticos()
        
        if entrada == 1:
            vx = speed
            vy = 0
            client.moveToZAsync(z,1).join()
            print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=90")
            client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 90)).join()
            time.sleep(3)
            vx = 0
            vy = speed
            print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy)+ ", yaw=180")
            client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 180)).join()
            time.sleep(3)
            vx = -speed
            vy = 0
            print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy)+ ", yaw=270")
            client.moveByVelocityZAsync(vx, vy, z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 270)).join()
            time.sleep(3)
            vx = 0
            vy = -speed
            print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=0")
            client.moveByVelocityZAsync(vx, vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
            time.sleep(3)
            
        if entrada == 2:
            numero = dp.gestosEstaticos()
            nav = orbit.OrbitNavigator(5, 5, 1, 1, [1,0], numero + 2)
            nav.start()
            
        if entrada == 3:
            client.simPrintLogMessage("Iniciando Rutina 2",severity=1)
            time.sleep(5)
            z=-6
            client.moveOnPathAsync([airsim.Vector3r(0,0,z),airsim.Vector3r(125,0,z),
                                        airsim.Vector3r(125,125,z),
                                        airsim.Vector3r(0,125,z),
                                        airsim.Vector3r(-125,125,z),
                                        airsim.Vector3r(-125,0,z)],
                                        6,110,
                                        airsim.DrivetrainType.ForwardOnly,airsim.YawMode(False,0),9,1)
        
            contador = 0
            while contador != 10:
                yoloFoto()
                time.sleep(1)
                contador = contador + 1
            
            
            
            client.moveToPositionAsync(0, 0, -5, 15).join()
                   
        
        if entrada == 4:
            client.rotateByYawRateAsync(36, 20)
            
            contador = 0
            while contador != 10:
                yoloFoto()
                time.sleep(2)
                contador = contador + 1
            
            
        if entrada == "Churros":
            print("Aterrizando")
            entrada1 = False
    

if verificar == False:
    print("Usuario no valido")  

client.hoverAsync().join()
client.landAsync().join()
print("Desarmando")
client.armDisarm(False)
client.enableApiControl(False)










