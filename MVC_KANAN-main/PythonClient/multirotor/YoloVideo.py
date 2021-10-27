import cv2
import numpy as np
import os
import time

tiempoLimite = 300
tiempoInicial=time.time()
tiempoActual=round(time.time()-tiempoInicial,3)

#inicio YOLO
#path1 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.weights'
#path2 = os.path.abspath(__file__)[:-10] + '/yolov2-tiny.cfg'
#net = cv2.dnn.readNet(path1, path2)
path1_1= os.path.abspath("yolov3.weights")
path2_1= os.path.abspath("yolov3.cfg")
print(path2_1)

net = cv2.dnn.readNet(path1_1, path2_1)



classes =  ["person","bicycle","car","motorbike","aeroplane","bus","car","truck","boat","traffic light","fire hydrant",
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
cap = cv2.VideoCapture("output2.avi")
outVideo = cv2.VideoWriter('outputYOLO2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1920,1080))

while True and tiempoActual<tiempoLimite:

    #responses = self.client.simGetImages([airsim.ImageRequest("low_res", airsim.ImageType.Scene, False, False)]) #scene vision image in png format
    #response = responses[0]
    #img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    #img_rgb = img1d.reshape(response.height, response.width, 3)

    #frames = img_rgb

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
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        for ii in range(len(boxes)):
            if ii in indexes:
                x, y, w, h = boxes[ii]
                m,n = centros[ii]
                cv2.rectangle(img, (x, y), (x + w, y + h), (231,130,35), 5)
                cv2.putText(img, classes[class_ids[ii]], (x, y-10), font, 1, (52,164,204), 2)

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
    outVideo.write(img)
    if cv2.waitKey(1) & 0xFF == ord('s'):             
        cap.release()
        cv2.destroyAllWindows()

    
    tiempoActual=round(time.time()-tiempoInicial,3)

outVideo.release()
cap.release()
cv2.destroyAllWindows()
