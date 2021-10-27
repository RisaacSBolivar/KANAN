import cv2
import time
import HandTrackingModule as htm
import depurado4

def gestosMov():
    cap=cv2.VideoCapture(0)

    doIt=True
    x=x2=x3=cont=0
    step1=step2=step3=False
    step1_1=step2_1=step3_1=False
    gesto1=gesto2=False
    
    detector = htm.handDetector(detectionCon=0.7)

    tipIds = [4, 8, 12, 16, 20]

    while True:
        success, img = cap.read()
        
        if doIt==True:
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            if len(lmList) !=0:
                fingers = []
                #Pulgar
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                #4 dedos
                for id in range(1,5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers=fingers.count(1)
                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

                ##########################################
                if x2==0 and x3==0 and totalFingers==5 and not gesto2:
                    if step1==False:
                        inicio1=time.time()
                        step1=True
                    x=round(time.time()-inicio1,2)
                    if 2>x>1:
                        gesto1=True
                    if x>2:
                        x=x2=x3=0
                        step1=False
                    cv2.putText(img,str(x)+" iniciando gesto 1" , (250,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
                    
                if x2==0 and x3==0 and totalFingers==0 and not gesto1:
                    if step1_1==False:
                        inicio1=time.time()
                        step1_1=True
                    x=round(time.time()-inicio1,2)
                    if 2>x>1:
                        gesto2=True
                    if x>2:
                        x=x2=x3=0
                        step1_1=False
                    cv2.putText(img, str(x)+" iniciando gesto 1" , (250,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)   
                ######################DESARROLLO GESTO ATENCION#################   
                if gesto1:
                    if(totalFingers==0):
                        if step2==False:
                            inicio2=time.time()
                            step2=True
                        x2=round(time.time()-inicio2,2)
                        if x>2:
                            x=x2=x3=0
                            step2=False
                        cv2.putText(img,str(x2) , (450,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
                        
                    if 2>x2>1 and totalFingers==5:
                        if step3==False:
                            inicio3=time.time()
                            step3=True
                        x3=round(time.time()-inicio3,2)
                        if x>2:
                            x=x2=x3=0
                            step2=False
                        cv2.putText(img, str(x3), (450,60), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)                
                    if 1.7>x3>1.5:
                        doIt=False
                        cont=200
                        cv2.destroyAllWindows();
                        cap.release();
                        if gesto1:
                            return depurado4.gestosEstaticos()
                        elif gesto2:
                            return 2
                ######################DESARROLLO GESTO ATENCION#################   
                if gesto2:
                    if(totalFingers==5):
                        if step2_1==False:
                            inicio2=time.time()
                            step2_1=True
                        x2=round(time.time()-inicio2,2)
                        if x>2:
                            x=x2=x3=0
                            step2_1=False
                        cv2.putText(img,str(x2) , (450,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
                        
                    if 2>x2>1 and totalFingers==0:
                        if step3_1==False:
                            inicio3=time.time()
                            step3_1=True
                        x3=round(time.time()-inicio3,2)
                        if x>2:
                            x=x2=x3=0
                            step2_1=False
                        cv2.putText(img, str(x3), (450,60), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)                
                    if 1.7>x3>1.5:
                        doIt=False
                        cont=200
                    ###########################
                    
                if totalFingers !=5:
                    step1=False
                    step3=False
                    step2_1=False
                    
                if totalFingers !=0:
                    step2=False
                    step1_1=False
                    step3_1=False
                    
                    
                    
        if cont>0:
            cont=cont-1
            if gesto1:
                cv2.putText(img, "Manda salida de GESTO 1", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
            elif gesto2:
                cv2.putText(img, "Manda salida de GESTO 2", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
            if cont==1:
                doIt=True
                x=x2=x3=0
                gesto1=gesto2=False
                
        cv2.imshow("Image", img)
        if cv2.waitKey(1)==27:

            cv2.destroyAllWindows();
            cap.release();
            break
        
def main():    
    print(gestosMov())
            
if __name__ == "__main__":
    main()
    
