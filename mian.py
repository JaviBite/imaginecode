#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import json

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from word2number import w2n
import pyttsx3

# obtain audio from the microphone
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('volume', 10.0)
engine.setProperty('rate', 115)

engine.say("Hola soy tu asistente de voz")
engine.runAndWait()

WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    # leer archivo

    with open('fichero.json') as json_file:
        data = json.load(json_file)

    cont_o = data["origin"]
    cont_d = data["destiny"]

    print(cont_d)
    print(cont_o)
    for d in cont_d:
        print(d["name"])
        for item in d["items"]:
            print(item["item"] + " " + str(item["n"]))


    while True:
        print("Say something!")

        #Mandar orden


        #Escuchar
        audio = r.listen(source)

        try:
            voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)
            print("Wit.ai thinks you said: " + voice_text)
            number = w2n.word_to_num(voice_text)
            print("Nums: " + str(number) )


        except ValueError:
            engine.say("No se ha reconocido nigun numero")
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # Tratar respuesta
