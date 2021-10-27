# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import math

def drawBox(img,bbox):
    ytc,xtc,_= img.shape
    xt = xtc
    yt = ytc
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    x_c=int((w/2)+x)
    y_c=int((h/2)+y)
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    
    cv2.circle(img,(x_c,y_c),4,(0,255,0),-1)
    cv2.circle(img,(int(xt/2),int(yt/2)),6,(0,0,255),-1)
    cv2.circle(img,(int(bbox[0]),int(bbox[1])),4,(0,0,255),-1)
    
    cv2.putText(img," Diff x= " + str(round(abs((xt/2)-x_c)/(xt/2),2)),(75,125),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2) #diferencia en x
    cv2.putText(img," Diff y= " + str(round(abs((yt/2)-y_c)/(yt/2),2)),(75,150),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2) #diferencia en y
    
def deteccionContinua():

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
    listabbox=[]
    while True:
        ret, frames = cap.read()
        if ret == False: break
        img= frames       
        height, width, channels = img.shape
        cont=cont+1   
        cc=cc+1
        x_ct = int(width/2)
        y_ct = int(height/2)

        if tracking:
            timer = cv2.getTickCount()
            success, img = cap.read()
            #success, bbox = tracker.update(img) #update
            success, boxes2 = tracker.update(img)
            if success:
                #drawBox(img,bbox)
                drawBox(img,boxes2)
                
            else:
                cv2.putText(img,"lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                
            fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
            cv2.putText(img,str(int((fps))),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            
        if not tracking:
        
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)    
            
            class_ids = []
            confidences = []
            boxes = []
            centros=[]
            cont = cont + 1
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
                font = cv2.FONT_HERSHEY_PLAIN
            
            arreglo = []
            diferencias = []
            ytc,xtc,_= img.shape
            xt = xtc
            yt = ytc
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
                    diferenciax = abs(round(((xt/2)-x_cen)/(xt/2),2))
                    diferenciay = abs(round(((yt/2)-y_cen)/(yt/2),2))
        
                    diferencias.append(diferenciax)
                    diferencias.append(diferenciay)
                    diferencias.append(x)
                    diferencias.append(y)
                    diferencias.append(w)
                    diferencias.append(h)
                    
                    ##########################################################
                    
                    #if word == classes[class_ids[ii]]:
                    #    cont = cont + 1
                    """if cont==5:
                     #   cont=0
                      #  bbox= boxes[ii]
                      #  tracking=True
                      #  tracker = cv2.legacy.TrackerMOSSE_create()
                      #  cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]),(0,255,0),2)
                      #  bbox = tuple(bbox)
                      #  tracker.init(img,bbox)"""
                    
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
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
                    cv2.putText(img, classes[class_ids[ii]], (x, y + 30), font, 2, (0,255,0), 2)
                    cv2.circle(img,(x_cen,y_cen),2,(0,255,0),-1)
                    cv2.putText(img, str(distancias.pop()), (x-5, y - 10), font, 1, (0,0,0), 1)
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
        try:
            maxiim = min(sumalista)
        except:
            print(sumalista)
            maxiim = sumalista[0]
        #print(sumalista)
        for i in range(len(sumalista)):
            if maxiim == sumalista[i]:
                indi = i  #indice donde esta el menor
                    
            #print(indi)
        #print("minimo valor",arreglo[indi][2],arreglo[indi][3])
        #cv2.circle(img,(arreglo[indi][2],arreglo[indi][3]),4,(0,0,255),-1)  #hay que pasarlo
        #boxes3 = []
        # =([arreglo[indi][2],arreglo[indi][3]])
        cv2.circle(img,(int(xt/2),int(yt/2)),6,(0,0,255),-1)
        boxes2 = []
        boxes2 = ([arreglo[indi][2],arreglo[indi][3], arreglo[indi][4], arreglo[indi][5]])            
        cv2.circle(img,(x_ct,y_ct),5,(0,0,255),-1)
        cv2.imshow('yolo',img)  
        if cont==10:  #tiempo que dura el yolo
                           
                #cap.release()
                #cv2.destroyAllWindows()
                
            #tracking = True
            tracking = True
            #bbox= boxes[distancias.index(min(distancias))]
            #cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]),(0,255,0),2)
            tracker = cv2.legacy.TrackerMOSSE_create()
            cv2.rectangle(img, (boxes2[0],boxes2[1]), (boxes2[2],boxes2[3]),(0,255,0),2)
            boxes2 = tuple(boxes2)
            print("boxes2",boxes2)
            tracker.init(img,boxes2) 
            listabbox.append(boxes2)
            print("listabbox",listabbox[0])
            
        if cv2.waitKey(1) & 0xFF == ord('q'):             
            cap.release()
            cv2.destroyAllWindows()
        
    cap.release()
    cv2.destroyAllWindows()


def main():
    deteccionContinua()

if __name__ == '__main__':
    try:
        main()
    except cv2.error as e:
        print(e)