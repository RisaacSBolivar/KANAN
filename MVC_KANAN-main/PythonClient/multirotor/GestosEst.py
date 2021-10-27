"""
Larios Hernández Jeremy Dimitri
"""
#En este, no hay  cero ni cinco. 
"""
Instrucciones:
Cada instrucción el programa lo confirma 4 segundos. En caso de que no haga el gesto durantre 4 segundos seguidos reinicia el conteo del tiempo
También una vez que ha detectado el programa el gesto y qué indicación va a hacer duerme el sistema 5 segundos para que el usuario baje su mano. 
Una vez que continua el programa el bucle vuelve a iniciar y continua
"""
import cv2
import time
from time import sleep #Biblioteca para detener la ejecución x segundos
import os
import HandTrackingModule as htm
import sys








def valores_nulos(): 
		global izquierda, uno, dos, tres, cuatro, churros, derecha, abajo, arriba
		izquierda=0
		uno = 0
		dos = 0
		tres = 0
		cuatro = 0
		churros = 0
		derecha = 0
		abajo = 0
		arriba = 0
		return izquierda, uno, dos, tres, cuatro, churros, derecha, abajo, arriba


def gestosEstaticos():

	global izquierda, uno, dos, tres, cuatro, churros, derecha, abajo, arriba

	wCam, hCam = 648, 480    #Esto es el tamaño de la cámara

	cap=cv2.VideoCapture(0)

	detector = htm.handDetector(detectionCon=0.7)

	izquierda=0
	uno = 0
	dos = 0
	tres = 0
	cuatro = 0
	churros = 0
	derecha = 0
	abajo = 0
	arriba = 0

	

	#Fnción para reiniciar los conteos de las acciones del drone y reiniciar el conteo cuango haga otro gesto. 


	while True:
		success, img = cap.read()
		img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
		lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList. 
		#print(lmList)

		if len(lmList) != 0:
	    
			#Mover el dron a la IZQUIERDA.
			if (lmList[4][1] > lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Dron se mueve a la izquierda", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				izquierda = izquierda + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = izquierda #Es necesario asignar el valor de izquierda a contador para que no se pierda el valor ya que en la siguiente instrucción izquierda es igual a 0, por lo que el contador se perdería. 
				valores_nulos()
				izquierda = contador #Le devolvemos el valor acumulado a izquierda. 
				contador = 0

            elif (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
                cv2.putText(img, "Control; Dedo pulgar, �ndice y medio, anularn y me�ique est�n abiertos. Todos los dem�s cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                control = control + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, as�, cuando el contador llegue a un x n�mero, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente.
                contador = control
                valores_nulos()
                control = contador
                contador = 0

			#Número 1:
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Número 1: Dedo índice abierto y todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				uno = uno + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = uno
				valores_nulos()
				uno = contador
				contador = 0
			#Número 2:
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Número 2: Dedo índice y medio están abiertos. Todos los demás cerrados. ", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				dos = dos + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = dos
				valores_nulos()
				dos = contador
				contador = 0
			#Número 3:
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Número 3: Dedo índice, medio y anular están abiertos. Todos los demás cerrados", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				tres = tres + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = tres
				valores_nulos()
				tres = contador
				contador = 0
			#Número 4
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
				cv2.putText(img, "Número 4: Dedo índice y medio, anularn y meñique están abiertos. Todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				cuatro = cuatro + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = cuatro
				valores_nulos()
				cuatro = contador
				contador = 0
			#Churros
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
				cv2.putText(img, "Churros; Dedo pulgar, índice y medio, anularn y meñique están abiertos. Todos los demás cerrados.", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				churros = churros + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = churros
				valores_nulos()
				churros = contador
				contador = 0
			#Mover dron a la DERECHA
			elif (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] > lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Derecha", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				derecha = derecha + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = derecha
				valores_nulos()
				derecha = contador
				contador = 0
			#Mover el dron hacia abajo. Gesto: dedo pulgar, índice y medio parados, anilar y meñique cerrados. 
			elif (lmList[4][1] > lmList[3][1]) and (lmList[8][2] < lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] > lmList[14][2]) and (lmList[20][2] > lmList[18][2]):
				cv2.putText(img, "Abajo", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				abajo = abajo + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = abajo
				valores_nulos()
				abajo = contador
				contador = 0
			#Mover hacia arriba. Abrir el meñique, anular y medio
			elif (lmList[4][1] < lmList[3][1]) and (lmList[8][2] > lmList[6][2]) and (lmList[12][2] < lmList[10][2]) and (lmList[16][2] < lmList[14][2]) and (lmList[20][2] < lmList[18][2]):
				cv2.putText(img, "Arriba", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				arriba = arriba + 1 #Al sumarle 1 lo que hago es que cuando repita el ciclo se vaya sumando 1 al gesto del pulgar, así, cuando el contador llegue a un x número, le deamos instrucciones para hacer. Cada 1 es 0.1 segundos aproximadamente. 
				contador = arriba
				valores_nulos()
				arriba = contador
				contador = 0
			else:
				cv2.putText(img, "Simbolo no introducido", (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
				izquierda, uno, dos, tres, cuatro, churros, derecha, abajo, arriba = 0,0,0,0,0,0,0,0,0 	#Si me da un símbolo o gesto inválido se reinicia el conteo. Aquí reinicio todos los acumuladores.

			#Instrucciones para el dron

			#Mover el dron a la izquierda
			if izquierda > 40:
				valores_nulos()
				cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
				cap.release();
				return "Izquierda"
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
			if derecha > 40: #Para mover el dron, si llego a poner la mano en ese sentido este conenzará a contar y cuando llegue el acumulador a 40 comenzará a moverse de inmediato.
				valores_nulos()
				cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
				cap.release();
				return "Derecha"
			if abajo > 40: #Para mover el dron, si llego a poner la mano en ese sentido este conenzará a contar y cuando llegue el acumulador a 40 comenzará a moverse de inmediato.
				valores_nulos()
				cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
				cap.release();
				return "Abajo"		
			if arriba > 40:
				valores_nulos()
				cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
				cap.release();
				return "Arriba"

		cv2.imshow("Image", img)
		cv2.waitKey(1)

		img = detector.findHands(img) #Esto nos muestra la mano. La detecta 
		lmList = detector.findPosition(img, draw=False)  #Esto encuentra la posición y la almacena en lmList. 

		if cv2.waitKey(1) == 27: #De esta forma podemos salir del bucle. Es 27 haciendo referencia  a la tecla scape. 
			
			cv2.destroyAllWindows();#Destruye todas las ventanas abuertas. 
			cap.release();
			break

def main():

	print(gestosEstaticos())

if __name__ == "__main__":
    main()
