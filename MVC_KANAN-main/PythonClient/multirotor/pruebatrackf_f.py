import setup_path
import airsim
import os
import sys
import math
import time
import argparse
from airsim.types import DrivetrainType, KinematicsState

import cv2
import numpy as np
import os
import math

import drone_lidar as ld


class Tracking:
   def __init__(self):
        """ Conecta con el cliente de Airsim, activa el control mediante API """
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.yawN = 0

        self.home = self.client.getMultirotorState().kinematics_estimated.position
        self.lidar = ld.Lidar()
        self.Vel = 0.3
        self.theta = 0

   def Despegue(self):
        """ Inicia el despegue del dron """
        self.client.simPrintLogMessage("Bienvenido, Iniciando KANAN",severity=2)
        print("Armando el drone")
        self.client.armDisarm(True)
        self.client.simPrintLogMessage("RETROCEDA POR FAVOR",severity=3)
        time.sleep(5)
        self.client.takeoffAsync().join()
        self.start = self.client.getMultirotorState().kinematics_estimated.position
        self.client.moveToZAsync(-10, 2)

        #yaw,pitch,roll=airsim.to_eularian_angles(self.client.getMultirotorState().kinematics_estimated.orientation)
        time.sleep(1)


   def drawBox(self,img,bbox):
        ytc,xtc,_= img.shape
        xt = xtc
        yt = ytc
        x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
        x_c=int((w/2)+x)
        y_c=int((h/2)+y)
        cv2.rectangle(img,(x,y),((x+w),(y+h)),(231,130,35),3,1)
        cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(52,164,204),2)
        
        cv2.circle(img,(x_c,y_c),4,(0,255,0),-1)
        cv2.circle(img,(int(xt/2),int(yt/2)),6,(0,0,255),-1)

        x = round(((xt/2)-x_c)/(xt/2),2)
        y = round(((yt/2)-y_c)/(yt/2),2)

        k=20

        pitch, roll, yaw  = airsim.to_eularian_angles(self.client.simGetVehiclePose().orientation)

        #yaw = math.degrees(yaw)
        print("yaw: ",yaw)


#--------------------------------------------------------------------------------------------------------

        print("pitch: ",pitch)
        print("roll: ",roll)

        altura = False

        print("yawN: ",self.yawN)
        self.client.rotateToYawAsync(self.yawN)

        self.lidar.build_windows()
        dis = self.lidar.windows.middle_center.min

        if 0.1>abs(x) :

            print("distancia: ",dis)
            if dis > 15:
                vx = math.cos(yaw)
                vy = math.sin(yaw)
                print("vx: " + str(vx))
                print("vy: " + str(vy))
                self.client.moveByVelocityAsync(vx,vy,0,0.1,airsim.DrivetrainType.ForwardOnly)
            if dis <=15:
                self.client.hoverAsync()
        else:
            self.yawN = self.yawN - (x)
            self.client.rotateByYawRateAsync(x*(-1)*40, 0.5)
            if abs(y)>=0.1 and altura==False:
                self.client.moveByVelocityZAsync(0,0,-y*k,0.1,airsim.DrivetrainType.MaxDegreeOfFreedom)
            else:
                altura = True

     #--------------------------------------------------------------------------------------------------------



        #vy = self.Vel*math.cos(math.radians(self.theta))
        #vx = self.Vel*math.sin(math.radians(self.theta))

        #print("vx: " + str(vx))
        #print("vy: " + str(vy))

        #self.client.moveByVelocityZAsync(vx,vy,-5,0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()

        #self.client.moveByVelocityZAsync(2,2,-5,1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
        #self.theta+=(-x*k)
        #print("theta: " + str(self.theta))
     #--------------------------------------------------------------------------------------------------------


        #cv2.putText(img," Diff x= " + str(x),(75,125),cv2.FONT_HERSHEY_SIMPLEX,0.7,(52,164,204),2)
        #cv2.putText(img," Diff y= " + str(y),(75,150),cv2.FONT_HERSHEY_SIMPLEX,0.7,(52,164,204),2)
        
   def deteccionContinua(self,word):
    
        path1_1= os.path.abspath("yolov3.weights")
        path2_1= os.path.abspath("yolov3.cfg")
    
        net = cv2.dnn.readNet(path1_1, path2_1)
        tracker = cv2.legacy.TrackerMOSSE_create()
            
        classes =  ["person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat","traffic light","fire hydrant",
                    "stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe",
                    "backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat",
                    "baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon",
                    "bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","sofa",
                    "pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone",
                    "microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier",
                    "toothbrush"]
    
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        cap = cv2.VideoCapture(0)
        
        cont=cc=0
        tracking=False
        bbox=[0,0,0,0]
    
        distancias=[]
        
        while True:

            responses = self.client.simGetImages([airsim.ImageRequest("low_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)

            frames = img_rgb

            #ret, frames = cap.read()
            ret = True

            if ret == False: break
            img= frames       
            height, width, channels = img.shape
            #cont=cont+1   
            cc=cc+1
            x_ct = int(width/2)
            y_ct = int(height/2)
    
            if tracking:
                timer = cv2.getTickCount()
                #success, img = cap.read()


                responses = self.client.simGetImages([airsim.ImageRequest("low_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
                response = responses[0]
                img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
                img_rgb = img1d.reshape(response.height, response.width, 3)

                img = img_rgb


                success, bbox = tracker.update(img) #update
                
                if success:
                    self.drawBox(img,bbox)
                else:
                    cv2.putText(img,"lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                    
                fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
                cv2.putText(img,str(int((fps))),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(52,164,204),2)
                
            if not tracking:
            
                blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)    
                
                class_ids = []
                confidences = []
                boxes = []
                centros=[]
                if cc==5:
                    distancias=[]
    
                #print("entra")
                for out in outs:
                    for detection in out:
                        
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            
                            # Object detected
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            
                            # Rectangle coordinates
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            centros.append([center_x,center_y])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    
                for ii in range(len(boxes)):
                    #distancias.append(100000)
                    #print(distancias)
                    #print("#########################################################")
                    if ii in indexes:   
                        x, y, w, h = boxes[ii]
                        m,n = centros[ii]
                        #centroide
                        x_cen = int((w/2)+x)
                        y_cen = int((h/2)+y)                    
                        distancias.append(round(math.sqrt((x_ct-x_cen)**2 + (y_ct-y_cen)**2),2))
                        
                        ##########################################################
                        
                        if word == classes[class_ids[ii]]:
                            cont = cont + 1
                        if cont==5:   #Cambiarlo despues
                            cont=0
                            bbox= boxes[ii]
                            tracking=True
                            tracker = cv2.legacy.TrackerMOSSE_create()
                            cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]),(231,130,35),2)
                            tracker.init(img,bbox)
                        
                        """if cont==14:
                            print("primera************************************")
                            cont=0
                            #return()
                            print(min(distancias))
                            print(distancias)
                            print(class_ids)
                            bbox= boxes[distancias.index(min(distancias))]
                            tracking=True
                            tracker = cv2.legacy.TrackerMOSSE_create()
                            cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]),(0,255,0),2)
                            tracker.init(img,bbox)"""
                        ############################################################
                        
                        cv2.circle(img,(x_cen,y_cen),4,(0,255,0),-1)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (52,164,204), 2)
                        cv2.putText(img, classes[class_ids[ii]], (x, y + 30), font, 2, (231,130,35), 2)
                        cv2.circle(img,(x_cen,y_cen),2,(52,164,204),-1)
                        cv2.putText(img, str(distancias.pop()), (x-5, y - 10), font, 1, (0,0,0), 1)
    
            cv2.circle(img,(x_ct,y_ct),5,(231,130,35),-1)
            cv2.imshow('yolo',img)  
            if cv2.waitKey(1) & 0xFF == ord('q'):             
                cap.release()
                cv2.destroyAllWindows()
            
        cap.release()
        cv2.destroyAllWindows()


def main():
    track = Tracking()
    track.Despegue()
    track.deteccionContinua("orange")
    #deteccionContinua("cell phone")

if __name__ == '__main__':
    try:
        main()
    except cv2.error as e:
        print(e)