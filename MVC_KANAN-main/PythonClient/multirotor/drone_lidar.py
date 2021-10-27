# Python client example to get Lidar data from a drone
#

import setup_path 
import airsim

import sys
import math
import time
import argparse
import pprint
import numpy

class Angles:
    def __init__(self):
        self.pitch = None           #vertical
        self.yaw = None             #horizontal
      
class Cell:
    def __init__(self,lista_datos,cell_dato):
        self.data = lista_datos
        self.cell = cell_dato
        if self.data == []:
            self.emtpy = True
            self.ndata = 0
            self.indmax= 0     #posicion del maximo
            self.max = 40              #valor del maximo
            self.indmin = 0   #posicion del minimo
            self.min = 40               #posicion del maximo 
            self.data_range = 0  #dif max - min
            self.median = 40   #mediana
            self.mean = 40       #promedio
            self.std = 0         #desviación estandar
            self.var = 0         #varianza
        else:
            self.emtpy = False
            self.ndata = numpy.array(self.data)
            self.indmax=numpy.argmax(self.ndata)     #posicion del maximo
            self.max = self.ndata.max()              #valor del maximo
            self.indmin = numpy.argmin(self.ndata)   #posicion del minimo
            self.min = self.ndata.min()               #posicion del maximo 
            self.data_range = numpy.ptp(self.ndata)  #dif max - min
            self.median = numpy.median(self.ndata)   #mediana
            self.mean = numpy.mean(self.ndata)       #promedio
            self.std = numpy.std(self.ndata)         #desviación estandar
            self.var = numpy.var(self.ndata)         #varianza
    
    
class Windows:
    def __init__(self,ul,uc,ur,ml,mc,mr,bl,bc,br):
        #print(len(ul))
        #print(len(uc))
        #print(len(ur))
        #print(len(ml))
        #print(len(mc))
        #print(len(mr))
        #print(len(bl))
        #print(len(bc))
        #print(len(br))
        self.upper_left=Cell(ul,1)
        self.upper_center=Cell(uc,2)
        self.upper_right=Cell(ur,3)
        self.middle_left=Cell(ml,4)
        self.middle_center=Cell(mc,5)
        self.middle_right=Cell(mr,6)
        self.bottom_left=Cell(bl,7)
        self.bottom_center=Cell(bc,8)
        self.bottom_right=Cell(br,9)
        self.shape = [[len(ul), len(uc), len(ur)],
                      [ len(ml), len(mc), len(mr)],
                      [ len(bl), len(bc), len(br)]] 

# Makes the drone fly and get Lidar data
class Lidar:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()  #Probar redundancia 
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.lidarData = None
        self.points = None
        self.position = None
        self.orientation = None
        self.indmax=None
        self.max = None
        self.indmin = None
        self.min = None
        self.data_range = None
        self.median = None
        self.mean = None
        self.std = None
        self.var = None
        self.angles = Angles()
        #self.angles.pitch = None
        #self.angles.yaw = None
        self.windows=None

    def execute(self):
        """Ejecuta una prueba armando el drone 
        con 5 tomas de lectura del lidar
        imprimiendo todos los valores"""
        print("arming the drone...")
        self.client.armDisarm(True)

        state = self.client.getMultirotorState()
        #s = pprint.pformat(state)
        #print("state: %s" % s)

        #airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()

        state = self.client.getMultirotorState()
        #print("state: %s" % pprint.pformat(state))

        #airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
        self.client.moveToPositionAsync(0, 0, -15, 5).join()

        self.client.hoverAsync().join()

        #airsim.wait_key('Press any key to get Lidar readings')
        
        for i in range(1,5):
            #lidarData = self.client.getLidarData();
            self.build_windows()
            #self.get_all(0,20)
            if (len(self.lidarData.point_cloud) < 3):
                print("\tNo points received from Lidar data")
            else:
                
                #points = self.parse_lidarData(lidarData)
                print("\n\n\tReading %d: time_stamp: %d number_of_points: %d" % (i, self.lidarData.time_stamp, len(self.points)))
                print("\t\tlidar position: %s" % (pprint.pformat(self.position)))
                print("\t\tlidar orientation: %s" % (pprint.pformat(self.orientation)))
                
                
                print("Primer punto: ",self.points[0])
                print("Numero de puntos :",self.points.shape)
                
                #Norma de los puntos en el lidar
                #norm = numpy.linalg.norm(points[0])
                #norm = numpy.linalg.norm(points[:20,:],axis=1)
                #self.get_norms(start=0,end=20)
                print("Normas calculadas: ",len(self.norms))
                print("Norma del primer punto: ",self.norms[0])
                
                print("\nNumero de ventanas: ",9)
                #print("\nVentana upper left: ")
                
                print("\n\n Ventanas: ")
                print(self.windows.shape)
                cell = self.windows.upper_center
                print("\nCelda: ",cell.cell)
                print("Empty: ",cell.emtpy)
                print("Indmax: ",cell.indmax)     #posicion del maximo
                print("Max: ",cell.max)              #valor del maximo
                print("Indmin: ",cell.indmin)   #posicion del minimo
                print("Min: ",cell.min)               #posicion del maximo 
                print("Rango: ",cell.data_range)  #dif max - min
                print("Mediana: ",cell.median)   #mediana
                print("Promedio: ",cell.mean)       #promedio
                print("Desviacin estandar: ",cell.std)         #desviación estandar
                print("Varianza: ",cell.var)         #varianza
                
                cell = self.windows.middle_center
                print("\nCelda: ",cell.cell)
                print("Empty: ",cell.emtpy)
                print("Indmax: ",cell.indmax)     #posicion del maximo
                print("Max: ",cell.max)              #valor del maximo
                print("Indmin: ",cell.indmin)   #posicion del minimo
                print("Min: ",cell.min)               #posicion del maximo 
                print("Rango: ",cell.data_range)  #dif max - min
                print("Mediana: ",cell.median)   #mediana
                print("Promedio: ",cell.mean)       #promedio
                print("Desviacin estandar: ",cell.std)         #desviación estandar
                print("Varianza: ",cell.var)         #varianza
                """
                print("\nIndice del maximo: ",self.windows.upper_left.indmax)   #posicion del maximo
                print("Maximo medido: ",self.windows.upper_left.max)           #valor del maximo
                print("Indice del minimo: ",self.windows.upper_left.indmin)   #posicion del minimo
                print("Minimo medido: ",self.windows.upper_left.min)           #posicion del maximo
                
                
                #Valores maximos y minimos
                print("\nIndice del maximo: ",self.indmax)   #posicion del maximo
                print("Maximo medido: ",self.max)           #valor del maximo
                print("Indice del minimo: ",self.indmin)   #posicion del minimo
                print("Minimo medido: ",self.min)           #posicion del maximo
                
                #Angulos 
                #print( math.atan(points[0,1]/points[0,0])) #Yaw
                #print( math.atan(points[0,2]/points[0,0])) #Pitch
                print("\nYaw punto 0: ",self.angles.yaw)
                print("Pitch punto 0: ",self.angles.pitch)
                
                
                #Estadística
                
                print("\nRango en los datos: ",self.data_range)
                print("Mediana: ",self.median)
                print("Promedio: ",self.mean)
                print("Desviacion estandar: ",self.std)
                print("Desviacion estandar: ",self.var)
                """
                
                time.sleep(5)
    
    def get_points(self):
        """Metodo para obtener los puntos medidos, asi como posicion y
        orientacion"""
        self.lidarData = self.client.getLidarData()
        self.points = self.parse_lidarData(self.lidarData)
        self.position = self.lidarData.pose.position
        self.orientation = self.lidarData.pose.orientation

    def get_pose(self):
        """Metodo para guardar la posicion y orientacion de los puntos"""
        if self.lidarData == None:
            self.get_points()
        self.position = self.lidarData.pose.position
        self.orientation = self.lidarData.pose.orientation
        
    def get_norms(self,start=0,end=None):
        """Metodo para obtener las normas de todos los puntos escaneados"""
        if self.lidarData == None:
            self.get_points()
        if end == None:
            end = len(self.points)
        self.norms = numpy.linalg.norm(self.points[start:end,:],axis=1)
    
    def get_a_norm(self,ind):
        """Metodo para obtener la norma de un punto en especifico, se debe
        enviar el indice del punto"""
        if self.lidarData == None:
            self.get_points()
        return numpy.linalg.norm(self.points[ind,:],axis=1)
    
    def get_angles(self):
        """Metodo para obtener los angulos pitch y yaw de todos los puntos"""
        if self.lidarData == None:
            self.get_points()
        self.angles.pitch = numpy.arctan(self.points[:,2]/self.points[:,0])
        self.angles.yaw = numpy.arctan(self.points[:,1]/self.points[:,0])
    
    def get_an_angle(self,ind=0):
        """Metodo para obtener el angulo de un punto en especifico,
        unicamente se debe mandar el indice de la medicion que se desea analizar"""
        return math.atan(self.points[ind,2]/self.points[ind,0]),math.atan(self.points[ind,2]/self.points[ind,0])
    
    def get_stadistics(self):
        """Este metodo obtiene los valores maximos y minimos
        así como sus indices y su diferencia. Tambien obtiene 
        la madiana, el promedio, la desviacion estandar y la varianza
        """
        if self.lidarData == None:
            self.get_points()
        self.indmax=numpy.argmax(self.norms)     #posicion del maximo
        self.max = self.norms.max()              #valor del maximo
        self.indmin = numpy.argmin(self.norms)   #posicion del minimo
        self.min = self.norms.min()              #posicion del maximo 
        self.data_range = numpy.ptp(self.norms)  #dif max - min
        self.median = numpy.median(self.norms)   #mediana
        self.mean = numpy.mean(self.norms)       #promedio
        self.std = numpy.std(self.norms)         #desviación estandar
        self.var = numpy.var(self.norms)         #varianza
        
    def build_windows(self):
        #self.windows = Windows()
        self.get_points()
        self.get_norms()
        self.get_angles()
        #print("yaw:",self.angles.yaw)
        #print("pitch",self.angles.pitch)
        yaw,pitch=0,0;
        l_upper_left=[]
        l_upper_center=[]
        l_upper_right=[]
        l_middle_left=[]
        l_middle_center=[]
        l_middle_right=[]
        l_bottom_left=[]
        l_bottom_center=[]
        l_bottom_right=[]
        for i in range(len(self.points)):
            #print(i,len(self.points),len(self.norms))
            #print(i)
            if self.angles.yaw[i] < -0.15 :
                yaw=1
            elif self.angles.yaw[i] < 0.15 :
                yaw=2
            else:
                yaw=3
            if self.angles.pitch[i] < 0.15 :
                pitch=1
            elif self.angles.pitch[i] < 0.35 :
                pitch=2
            else:
                pitch=3
            if yaw == 1 and pitch == 1:
                l_upper_left.append(self.norms[i])
            elif yaw == 1 and pitch == 2:
                l_middle_left.append(self.norms[i])
            elif yaw == 1 and pitch == 3:
                l_bottom_left.append(self.norms[i])
            elif yaw == 2 and pitch == 1:
                l_upper_center.append(self.norms[i])
            elif yaw == 2 and pitch == 2:
                l_middle_center.append(self.norms[i])
            elif yaw == 2 and pitch == 3:
                l_bottom_center.append(self.norms[i])
            elif yaw == 3 and pitch == 1:
                l_upper_right.append(self.norms[i])
            elif yaw == 3 and pitch == 2:
                l_middle_right.append(self.norms[i])
            elif yaw == 3 and pitch == 3:
                l_bottom_right.append(self.norms[i])
        self.windows = Windows(l_upper_left,l_upper_center,l_upper_right,l_middle_left,
                               l_middle_center, l_middle_right, l_bottom_left,
                               l_bottom_center, l_bottom_right)
    
    def get_all(self,norms_start=0,norms_end=None):
        """Metodo para obtener los puntos, normas, rangos, y estadisticas"""
        self.get_points()
        self.get_norms(norms_start,norms_end)
        self.get_angles()
        self.get_stadistics()
    
    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def write_lidarData_to_disk(self, points):
        # TODO
        print("not yet implemented")

    def stop(self):

        #airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

# main
if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    arg_parser = argparse.ArgumentParser("Lidar.py makes drone fly and gets Lidar data")

    arg_parser.add_argument('-save-to-disk', type=bool, help="save Lidar data to disk", default=False)
  
    args = arg_parser.parse_args(args)    
    lidarTest = Lidar()
    try:
        lidarTest.execute()
    finally:
        lidarTest.stop()
