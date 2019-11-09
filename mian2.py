#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import json
from enum import Enum

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from word2number import w2n
import pyttsx3

import os

# obtain audio from the microphone
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('volume', 10.0)
engine.setProperty('rate', 115)

class Boxes(Enum):
    Pink = 1 #Rosa
    Green = 2 #Verde
    Yellow = 3 #Amarillo
    Blue = 4 #Azul
    Red = 5 #Rojo
    White = 6 #Blanco
    Black = 7 #Negro
    Orange = 8 #Naranja
    Purple = 9 #Morado
    Brown = 10 #Marron
    Grey = 11 #Gris
    Silver = 12 #Plateado
    Gold = 13 #Dorado
    Beige = 14 #Beige
    Lilac = 15 #Lila
    Light_blue = 16 #Azul clarito
    Dark_blue = 17 #Azul oscuro
    Violeta = 18 #Violet
    Turqoise = 19 #Turquesa
    Magenta = 20 #Magenta

engine.say("Hola soy tu asistente de voz")
engine.runAndWait()

WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings


# Detecta el color de la caja
def contains_color(voice_text):
    for color in Boxes:
        if color in voice_text:
            return color


# El color de la caja de destino será el detectado
def Search(voice_text):
    if "destiny" in voice_text:
        for box in cont_d:
            color = contains_color(voice_text)


def searchfor(cont, item_to):
    for box in cont:
        for item in box["items"]:
             print(item["name"])
             if item["name"] == item_to:
                 return box["name"]
    return "NONE"


def order(cont_d, cont_o):
    for box in cont_d:
        for item in box["items"]:
            num = item["n"]
            if num > 0:
                box_to_search = searchfor(cont_o, item["name"])
                if box_to_search != "NONE":
                    return "Pick up " + str(num) + " " + item["name"] + ("s" if num > 1 else "") + " from origin box" + box_to_search

    return "ERROR"

def orderDest(cont_d, name_d, number, cont_o):
    for box in cont_d:
        for item in box["items"]:
            if item["name"] == name_d and item ["n"]!=0:
                if item["n"] >= number:
                    item["n"] = item["n"] - number
                    return "Put " + str(number) + " " + item["name"] + " into the " + box["name"] + " box"
                else:
                    aDev = "Put " + str(item["n"]) + " " + item["name"] + " into the " + box["name"] + " box and leave the rest one at the origin " + cont_o["name"]
                    item["n"] = 0
                    return aDev

    return "There are not " + str(number) + " " + item["name"] + " into the " + box["name"] + " box"



with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    # leer archivo

    with open('fichero.json') as json_file:
        data = json.load(json_file)

    cont_o = data["origin"]
    cont_d = data["destiny"]

    # print(cont_d)
    # print(cont_o)
    # for d in cont_d:
    #     print(d["name"])
    #     for item in d["items"]:
    #         print(item["item"] + " " + str(item["n"]))


    while True:
        print("Say something!")

        #Mandar orden
        ord = order(cont_d, cont_o)
        engine.say(ord)
        print(ord + "\n")
        engine.runAndWait()



        #Escuchar
        audio = r.listen(source)

        WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)

            number = w2n.word_to_num(voice_text)
            print("Nums: " + str(number) )


            for box in cont_o:
                for item in box["items"]:
                  if item["name"] in voice_text:
                      ordDest = orderDest(cont_d, item["name"], number, box["name"])
                      engine.say(ordDest)
                      print(ordDest + "\n")
                      engine.runAndWait()



            print("Creo que has dicho: " + voice_text)
            engine.say(voice_text)
            engine.runAndWait()




        except ValueError:
            engine.say("No se ha reconocido ningun numero")

        except sr.UnknownValueError:
            engine.say("Lo siento, no he entendido lo que has dicho")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # Tratar respuesta
