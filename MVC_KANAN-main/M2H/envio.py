# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 18:23:44 2021

@author: ASUS
"""

from telebot_Kanan import enviar_foto, enviar_mensaje, tb

texto = "Hola Jeremy"
enviar_mensaje(texto)
direc = "../Reconocimiento_rostros/ImagesAttendance/jeremy.png"
enviar_foto(direc)

#Comunicación asíncrona
@tb.message_handler(commands=['start', 'help'])#Con estos comandos se activa la comunicación humano - máquina
def send_welcome(message):
	tb.reply_to(message, """Selecciona una opción:
1. Saludar
2. Despedir
    """)
 
@tb.message_handler(func=lambda message: True)
def echo_all(message):
    if int(message.text)==1:
        tb.reply_to(message, "Hola")
    elif int(message.text)==2:
        tb.reply_to(message, "Adios")
    else:
        tb.reply_to(message, "Jaja, bien intento, terrícola")

tb.polling()    
    