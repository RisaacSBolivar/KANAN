
import telebot
import os

TOKEN = '1820335491:AAHkGSRICz6wGeaPqbPv4SPZRW2fthRIDR8'

KANAN_ID = -275364205

tb = telebot.TeleBot(TOKEN)
    
#chats = [1612656491, 1887945366]#Jonathan, Angel

chats = {"ANGEL":1887945366,"YAIR":1612656491,"chatG":KANAN_ID}



def enviar_mensaje(mensaje,piloto):
    mandar = str(mensaje)
    tb.send_message(chats[piloto], mandar)


def enviar_foto(nombre,piloto):
    path1_1= os.path.abspath(nombre)
    photo = open(path1_1, 'rb')
    tb.send_photo(chats[piloto], photo)

def enviar_video(videoN,piloto):
    path1_1= os.path.abspath(videoN)
    photo = open(path1_1, 'rb')
    tb.send_video(chats[piloto],photo)



#enviar_foto("photo_0.png")

#enviar_video("output.avi","YAIR")

#No se puede  mandar un mensaje con imagen y texto, es necesario mandarlos separados
#https://stackoverflow.com/questions/37860889/sending-message-in-telegram-bot-with-images/37864971
    
