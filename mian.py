#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from enum import Enum
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

with sr.Microphone() as source:

    # leer archivo

    cont_o = [{
            "name": "blue",
            "items": {
                "item": "glass",
                "n": 5
            }
        },
        {
            "name": "pink",
            "items": {
                "item": "coco",
                "n": 3
            }
        }
    ]

    cont_d = [
     {
        "name": "blue",
        "items": [
            {
                "item": "glass",
                "n": 3
            },
            {
                "item": "coco",
                "n": 1
            }
        ]
    },
    {
        "name": "blue",
        "items": [
            {
                "item": "glass",
                "n": 2
            },
            {
                "item": "coco",
                "n": 2
            }
        ]
    }]

    print(cont_d)
    print(cont_o)
    for d in cont_d:
        print(d["name"])
        for item in d["items"]:
            print(item["item"] + " " + str(item["n"]))


    while True:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)

            number = w2n.word_to_num(voice_text)
            print("Nums: " + str(number) )

            print("Creo que has dicho: " + voice_text)
            engine.say(voice_text)
            engine.runAndWait()


        except ValueError:
            engine.say("No se ha reconocido nigun numero")

        except sr.UnknownValueError:
            engine.say("Lo siento, no he entendido lo que has dicho")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))


# Detecta el color de la caja
def contains_color (voice_text):
    for color in Boxes:
        if color in voice_text:
            return color

# El color de la caja de destino será el detectado
def Search(voice_text):
    if "destiny" in voice_text:
        for box in cont_d:
            color = contains_color(voice_text)
