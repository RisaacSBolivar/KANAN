# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import mediapipe as mp
import math

def deteccionContinua():

  
    path1_1 = "yolov3.weights"
    path2_1 = "yolov3.cfg"
    coord = []
    control = []
    #arreglo = []
    arregloo = []
    arreglo2 = []
    arreglo3 =[]
    arreglo_control = []
    coordxy = []
    #diferencias = []
    
    
    
    #print(path2_1)
    net = cv2.dnn.readNet(path1_1, path2_1)
        
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
    
    cont=0
    
    while True:
        ret, frames = cap.read()
        if ret == False: break           
    
        img= frames       
        
        xtc,ytc,_= img.shape
        xt = xtc + 130
        yt = ytc -130
        
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)    
        
        class_ids = []
        confidences = []
        boxes = []
        centros=[]

        cont=cont+1   
        #xt,yt,_= img.shape
        
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
            
            font = cv2.FONT_HERSHEY_PLAIN
            arreglo = []
            diferencias = []
            for ii in range(len(boxes)):
                
                coord=[]
                if ii in indexes:
                    coord=[]
                    x, y, w, h = boxes[ii]
                    m,n = centros[ii]
                    #centroide de cada objeto
                    x_cen = int((w/2)+x)
                    y_cen = int((h/2)+y)
            
                    cv2.circle(img,(x_cen,y_cen),4,(0,255,0),-1)
                    
                    
                   
                    
                    coord.append(x_cen)
                    coord.append(y_cen)
                    
                    control.append(x)
                    control.append(y)
                    control.append(w)
                    control.append(h)
                    
                    
                    
                    
                    arreglo_control.append(control)
                    #diferencia de centroide con respecto al punto medio
                    diferenciax = abs(round(((xt/2)-x_cen)/(xt/2),2))
                    diferenciay = abs(round(((yt/2)-y_cen)/(yt/2),2))
    
                    diferencias.append(diferenciax)
                    diferencias.append(diferenciay)
                    diferencias.append(x)
                    diferencias.append(y)
                    diferencias.append(w)
                    diferencias.append(h)
                  
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
                    cv2.putText(img, classes[class_ids[ii]], (x, y + 30), font, 2, (0,255,0), 2)      
                    cv2.circle(img,(x_cen,y_cen),4,(0,255,0),-1)
                    #cv2.putText(img," Diff x= " + str(diferenciax),(75,175),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                    #cv2.putText(img," Diff y= " + str(diferenciay),(75,275),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            
                    
                    arreglo.append(diferencias)

                    diferencias = []
           
            
        
        print("*******************arreglo***********",len(arreglo))
        print(arreglo)
        sumalista = []
        indi = 0
        for i in range(len(arreglo)):
             ar = arreglo[i]
             a = ar[0]
             b = ar[1]
             a_cuadrada = a**2
             b_cuadrada = b**2
             
             suma = math.sqrt(a_cuadrada+b_cuadrada)
             
             sumalista.append(suma)
        maxiim = min(sumalista)
        #print(sumalista)
        for i in range(len(sumalista)):
            if maxiim == sumalista[i]:
                indi = i  #indice donde esta el menor
                
        #print(indi)
        print("minimo valor",arreglo[indi][2],arreglo[indi][3])
        cv2.circle(img,(arreglo[indi][2],arreglo[indi][3]),4,(0,0,255),-1)  #hay que pasarlo
        cv2.circle(img,(int(xt/2),int(yt/2)),6,(0,0,255),-1)
        boxes2 = []
        boxes2 = ([arreglo[indi][2],arreglo[indi][3], arreglo[indi][4], arreglo[indi][5]])
        cv2.imshow('yolo',img)   
        
        if cont==10:  #tiempo que dura el yolo
                       
            cap.release()
            cv2.destroyAllWindows()
            return (boxes2) 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):             
            cap.release()
            cv2.destroyAllWindows()
          
       
       
    
    cap.release()
    cv2.destroyAllWindows()

def tracking(bb_arg):
    cap = cv2.VideoCapture(0)
    
    tracker = cv2.legacy.TrackerMOSSE_create()
    succes, img = cap.read()
    
    xtc,ytc,_= img.shape
    xt = xtc + 130
    yt = ytc -130
    
    
    b=[]
    
    bbox=bb_arg
    
    
    
    cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]),(0,255,0),2)
    tracker.init(img,bbox)
    
    def drawBox(img,bbox):
        x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
        x_c=int((w/2)+x)
        y_c=int((h/2)+y)
        cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
        cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        cv2.circle(img,(x_c,y_c),4,(0,255,0),-1)
        cv2.circle(img,(int(xt/2),int(yt/2)),6,(0,0,255),-1)
        
        cv2.putText(img," Diff x= " + str(round(abs((xt/2)-x_c)/(xt/2),2)),(75,175),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        cv2.putText(img," Diff y= " + str(round(abs((yt/2)-y_c)/(yt/2),2)),(75,275),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
            
    
    while True:
        timer = cv2.getTickCount()
        success, img = cap.read()
        
        success, bbox = tracker.update(img) #update
        
        
        if success:
            drawBox(img,bbox)
        else:
            cv2.putText(img,"lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            
        
        fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
        cv2.putText(img,str(int((fps))),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        
        cv2.imshow("Frame",img)        
     
        if cv2.waitKey(1) & 0xff == ord('q'):
            break        
    cap.release()
    cv2.destroyAllWindows()


def main():
    b=deteccionContinua()
    print(b)
    
    b1=b[0]
    b2=b[1]
    b3=b[2]
    b4=b[3]
    bf=(b1,b2,b3,b4)
    print(bf)
    
    tracking(bf)

if __name__ == '__main__':
    try:
        main()
    except cv2.error as e:
        print(e)