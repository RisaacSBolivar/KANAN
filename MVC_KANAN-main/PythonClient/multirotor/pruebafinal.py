import cv2
import time
from time import sleep #Biblioteca para detener la ejecución x segundos
import os
import HandTrackingModule as htm
import sys
import mediapipe as mp






def valores_nulos(): 
	global control, uno, dos, tres, cuatro, churros
	control = 0
	uno = 0
	dos = 0
	tres = 0
	cuatro = 0
	churros = 0

	return control, uno, dos, tres, cuatro, churros



def gestosEstaticos():


    global control, uno, dos, tres, cuatro, churros, retorno

    #wCam, hCam = 648, 480#Esto es el tamaño de la cámara

    cap=cv2.VideoCapture(0)

    detector = htm.handDetector(detectionCon=0.7)




    control = 0
    uno = 0
    dos = 0
    tres = 0
    cuatro = 0
    churros = 0
	
	#Fadul
    doIt=True



    while True:
        success, img = cap.read()
        img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
        lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList. 
  		#print(lmList)
  
        if doIt==True:
  
            if len(lmList) != 0:
                #fingers = []
  
  				#Control del dron manualmente
                if (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                    cv2.putText(img, "Control Continuo", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    control = control + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
                    contador = control
                    valores_nulos()
                    control = contador
                    contador = 0
  				#Número 1:
                elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
                    cv2.putText(img, "1 - Grabacion", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    uno = uno + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                    contador = uno
                    valores_nulos()
                    uno = contador
                    contador = 0
  				#Número 2:
                elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
                    cv2.putText(img, "2 - Orbita", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    dos = dos + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                    contador = dos
                    valores_nulos()
                    dos = contador
                    contador = 0
  				#Número 3:
                elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
                    cv2.putText(img, "3 - Reconocimiento de Objetos", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    tres = tres + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                    contador = tres
                    valores_nulos()
                    tres = contador
                    contador = 0
  				#Número 4
                elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                    cv2.putText(img, "4 - Active Tracking", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    cuatro = cuatro + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                    contador = cuatro
                    valores_nulos()
                    cuatro = contador
                    contador = 0
  				#Churros
                elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                    cv2.putText(img, "Salir", (140,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (231,130,35), 3)
                    churros = churros + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                    contador = churros
                    valores_nulos()
                    churros = contador
                    contador = 0
                else:
                    uno, dos, tres, cuatro, churros = 0,0,0,0,0 #Si me da un símbolo o gesto inválido se reinicia el conteo. Aquí reinicio todos los acumuladores.
  

  
  				#Instrucciones para el gesto del número 1 con el índice:
                if uno > 40: #Cuando el acumulador del uno llegue a 41 lo que hará es realizar las instrucciones debidas.
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return 1
  				#Instrucciones para el gesto con el número 2:
                if dos > 40:
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return 2
  				#Instrucciones para el gesto con el número 3:
                if tres > 40:
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return 3
                if cuatro > 40:
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return 4
                if churros > 40:
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return "Churros"
                if control > 40:
                    valores_nulos()
                    cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
                    cap.release();
                    return "Control"

  
        cv2.imshow("Image", img)
        cv2.waitKey(1)
  
        img = detector.findHands(img) #Esto nos muestra la mano. La detecta
        lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList.
  
        if cv2.waitKey(1) == 27: #De esta forma podemos salir del bucle. Es 27 haciendo referencia  a la tecla scape.
            cv2.destroyAllWindows();#Destruye todas las ventanas abuertas.
            cap.release();
            break
