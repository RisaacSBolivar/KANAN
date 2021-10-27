import cv2
import numpy as np
import os
import time


def deteccionContinua(tiempoLimite):
    tiempoInicial=time.time()
    tiempoActual=round(time.time()-tiempoInicial,3)

    #inicio YOLO
    #path1 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.weights'
    #path2 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.cfg'
    #net = cv2.dnn.readNet(path1, path2)
    
    path1_1 = os.path.abspath(__file__)[:-10] + '/yolov3.weights'
    path2_1 = os.path.abspath(__file__)[:-10] + '\yolov3.cfg'
    net = cv2.dnn.readNet(path1_1, path2_1)
    
    

    classes =  ["person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat","traffic light","fire hydrant",
                "stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe",
                "backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat",
                "baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon",
                "bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","sofa",
                "pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone",
                "microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier",
                "toothbrush"]
    tiempos = [0] * 80
    detecciones=["index0"]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    cap = cv2.VideoCapture(0)

    while True and tiempoActual<tiempoLimite:
        ret, frames = cap.read()
        if ret == False: break           
    
        img= frames       
        
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)    
        
        class_ids = []
        confidences = []
        boxes = []
        centros=[]        
            
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
            for ii in range(len(boxes)):
                if ii in indexes:
                    x, y, w, h = boxes[ii]
                    m,n = centros[ii]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
                    cv2.putText(img, classes[class_ids[ii]], (x, y + 30), font, 2, (0,255,0), 2)
                    
                    if tiempos[class_ids[ii]]==0:
                        tiempos[class_ids[ii]]=time.time()
                        if detecciones[-1]=="index0":
                            detecciones.pop()
                            detecciones.append(classes[class_ids[ii]])
                        if detecciones[-1]!=classes[class_ids[ii]]:
                            detecciones.append(classes[class_ids[ii]])
                    if (tiempos[class_ids[ii]] -time.time())>10:
                        tiempos[class_ids[ii]]=0

        cv2.imshow('yolo',img)  
        
        if cv2.waitKey(1) & 0xFF == ord('s'):             
            cap.release()
            cv2.destroyAllWindows()
            return detecciones
        
        tiempoActual=round(time.time()-tiempoInicial,3)
        
    cap.release()
    cv2.destroyAllWindows()
    return detecciones

def deteccionUnica(img_):
    cap = cv2.VideoCapture(0)
    ret, frames = cap.read()
    if ret == False: print("algo salió mal")          
    img= frames
    detecciones=[]
    
    path1 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.weights'
    path2 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.cfg'
    net = cv2.dnn.readNet(path1, path2)

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
    
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)    
    
    class_ids = []
    confidences = []
    boxes = []
    centros=[]        
        
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
        for ii in range(len(boxes)):
            if ii in indexes:
                x, y, w, h = boxes[ii]
                m,n = centros[ii]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
                cv2.putText(img, classes[class_ids[ii]], (x, y + 30), font, 2, (0,255,0), 2)
                
                detecciones.append(classes[class_ids[ii]])
                
    cv2.imshow('yolo',img)  
        
    cap.release()
    cv2.destroyAllWindows()
    return detecciones



def yolo(opcion,tiempoLimite):
    if opcion==1:
        return deteccionContinua(tiempoLimite)
    if opcion==2:
        return deteccionUnica(tiempoLimite)


def main():
    tiempoLimite=10.0
    print(yolo(1,tiempoLimite))

if __name__ == '__main__':
    try:
        main()
    except cv2.error as e:
        print(e)

