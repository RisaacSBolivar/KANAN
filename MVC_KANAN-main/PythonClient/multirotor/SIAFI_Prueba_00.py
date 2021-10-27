############################################
################### KANAN ##################
############################################

#*************************************************************************************
#*************************************************************************************
import setup_path
import airsim
#*************************************************************************************
#*************************************************************************************
import sys
import math
import time 
import argparse
import numpy
#import numpy as np
#-------------------------------------------------------------------------------------
#import pprint
#import cv2
#import os 
#import tempfile
#-------------------------------------------------------------------------------------


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#Conectarse al simulador
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)





#-------------------------------------------------------------------------------------

    #Armado y espera a que el usuario se mueva
a = int(input("Elige el movimiento: "))
if a == 1:
    print("Armando el drone")
    client.armDisarm(True)
    time.sleep(10)
        

#-------------------------------------------------------------------------------------
#Despegue y comprobacion 
#state = client.getMultirotorState()
#if state.landed_state == airsim.LandedState.Landed:
#    print("Despegando")
#    client.takeoffAsync().join()
#else:
#    client.hoverAsync().join()

client.takeoffAsync(20, ).join()
#client.hoverAsync().join()

time.sleep(10)
state = client.getMultirotorState()

#if state.landed_state == airsim.LandedState.Landed:
#    print("Despegue Fallido")
#    sys.exit(10)
#-------------------------------------------------------------------------------------
#Vuelo
time.sleep(10)
z = -10
time.sleep(10)
client.moveToZAsync(z, 1).join()
#-------------------------------------------------------------------------------------
#Aterrizaje 

time.sleep(10)
client.moveToPositionAsync(0,0,z,1).join()
print("Aterrizando")
client.landAsync().join()
print("Desarmando")
client.armDisarm(False)
client.enableApiControl(False)





