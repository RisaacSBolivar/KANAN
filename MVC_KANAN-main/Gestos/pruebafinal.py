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

	wCam, hCam = 648, 480    #Esto es el tamaño de la cámara

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
	x=x2=x3=cont=0
	step1=step2=step3=False
	step1_1=step2_1=step3_1=False
	gesto1=gesto2=False
	tipIds = [4, 8, 12, 16, 20]

	while True:
		success, img = cap.read()
		img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
		lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList. 
		#print(lmList)

		if doIt==True:

			if len(lmList) != 0:
				fingers = []

				#Control del dron manualmente
				if (control <40 and lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
					cv2.putText(img, "Control; Dedo pulgar, índice y medio, anularn y meñique están abiertos. Todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					control = control + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = control
					valores_nulos()
					control = contador
					contador = 0
				#Número 1:
				elif (control < 40 and lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
					cv2.putText(img, "Número 1: Dedo índice abierto y todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					uno = uno + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = uno
					valores_nulos()
					uno = contador
					contador = 0
				#Número 2:
				elif (control < 40 and lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
					cv2.putText(img, "Número 2: Dedo índice y medio están abiertos. Todos los demás cerrados. ", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					dos = dos + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = dos
					valores_nulos()
					dos = contador
					contador = 0
				#Número 3:
				elif (control < 40 and lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
					cv2.putText(img, "Número 3: Dedo índice, medio y anular están abiertos. Todos los demás cerrados", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					tres = tres + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = tres
					valores_nulos()
					tres = contador
					contador = 0
				#Número 4
				elif (control < 40 and lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
					cv2.putText(img, "Número 4: Dedo índice y medio, anularn y meñique están abiertos. Todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					cuatro = cuatro + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = cuatro
					valores_nulos()
					cuatro = contador
					contador = 0
				#Churros
				elif (control < 40 and lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
					cv2.putText(img, "Churros; Dedo pulgar, índice y medio, anularn y meñique están abiertos. Todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					churros = churros + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
					contador = churros
					valores_nulos()
					churros = contador
					contador = 0
				else:
					uno, dos, tres, cuatro, churros = 0,0,0,0,0 #Si me da un símbolo o gesto inválido se reinicia el conteo. Aquí reinicio todos los acumuladores.

				#INSTRUCCIONES PARA EL DRON
				#Controlar dron manualmente

				#Izquierda
				if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]) and (lmList[1][2] < lmList[0][2]) and (lmList[4][1] > lmList[3][1]): #este último es para que el número 4 sea mayor a 3 de izquierda a derecha en la pantalla
					cv2.putText(img, "Izquierda", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					print("Dron se mueve a la izquierda")
					retorno = "izquierda"
				#Dron se mueve hacia arriba
				if (control == 40) and (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]) and (lmList[1][2] < lmList[0][2]):
					cv2.putText(img, "Arriba", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					print("Dron se nueve hacia arriba")
					retorno = "arriba"
				#Dron se mueve hacia la derecha
				if (control == 40) and (lmList[4][1] < lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]) and (lmList[1][2] < lmList[0][2]) and (lmList[17][1] > lmList[13][1]):
					cv2.putText(img, "Derecha", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					print("Dron se mueve a la derecha")
					retorno = "derecha"
				#Dron se mueve hacia abajo
				if (control == 40) and (lmList[0][2] < lmList[4][2]): #el 2es del eje y
					cv2.putText(img, "Abajo", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
					print("Dron Abajo")
					retorno = "abajo"
				#Fadul:
				#FINALIZAR CONTROL MANUAL DEL DRON
				#Pulgar
				if (lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]) and (control == 40):
					fingers.append(1)
				else:
					fingers.append(0)
				#4 dedos
				for id in range(1,5):
					if (lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]) and (control == 40):
						fingers.append(1)
					else:
						fingers.append(0)

				totalFingers=fingers.count(1)

				if x2==0 and x3==0 and totalFingers==0 and not gesto1 and (control == 40):
					if step1_1==False:
						inicio1=time.time()
						step1_1=True
					x=round(time.time()-inicio1,2)
					if 2>x>1:
						gesto2=True 
					if x>2:
						x=x2=x3=0
						step1_1=False
					cv2.putText(img, str(x)+" iniciando gesto 2" , (250,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
				###
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
					####
				if totalFingers !=5:
					step1=False
					step3=False
					step2_1=False
				if totalFingers !=0:
					step2=False
					step1_1=False
					step3_1=False

				#Instrucciones para el gesto del número 1 con el índice:
				if uno > 40: #Cuando el acumulador del uno llegue a 41 lo que hará es realizar las instrucciones debidas. 
					valores_nulos()
					cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
					cap.release();
					return "Uno: En esta parte daremos las instrucciones al drone"
				#Instrucciones para el gesto con el número 2:
				if dos > 40:
					valores_nulos()
					cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
					cap.release();
					return "Dos: En esta parte daremos las instrucciones al drone"
				#Instrucciones para el gesto con el número 3:
				if tres > 40:
					valores_nulos()
					cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
					cap.release();
					return "Tres: Dron hace rutina"
				if cuatro > 40:
					valores_nulos()
					cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
					cap.release();
					return "Cuatro: Dron hace rutina"
				if churros > 40:
					valores_nulos()
					cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
					cap.release();
					return "Churros: Dron Hace rutina"
		#Fadul:
		#Aqui se finaliza el contro manual
		if cont>0:
			cont=cont-1
			if gesto2:
				cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
				cap.release();
				return "Termina control"
			if cont==1:
				doIt=True
				x=x2=x3=0
				gesto1=gesto2=False		

		cv2.imshow("Image", img)
		cv2.waitKey(1)

		img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
		lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList. 

		if cv2.waitKey(1) == 27: #De esta forma podemos salir del bucle. Es 27 haciendo referencia  a la tecla scape. 
			
			cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
			cap.release();
			break