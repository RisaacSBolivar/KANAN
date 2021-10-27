# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 23:32:02 2021

@author: ASUS
"""

#'''
import telebot

KANAN_ID = -275364205
TOKEN = '1820335491:AAHkGSRICz6wGeaPqbPv4SPZRW2fthRIDR8'
tb = telebot.TeleBot(TOKEN)
    
chats = [1612656491, 1887945366]#Jonathan, Angel

def enviar_mensaje(mensaje):
    mandar = str(mensaje)
    tb.send_message(KANAN_ID, mandar)


def enviar_foto(direccion):
    photo = open(direccion, 'rb')
    tb.send_photo(KANAN_ID, photo)
    
#No se puede  mandar un mensaje con imagen y texto, es necesario mandarlos separados
#https://stackoverflow.com/questions/37860889/sending-message-in-telegram-bot-with-images/37864971
    
