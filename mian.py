#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from word2number import w2n
import pyttsx3

class cont:
    name = ""
    items = ""
    n = 0

# obtain audio from the microphone
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('volume', 10.0)
engine.setProperty('rate', 115)

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
            print("Wit.ai thinks you said: " + voice_text)
            number = w2n.word_to_num(voice_text)
            print("Nums: " + str(number) )
            engine.say(voice_text)
            engine.runAndWait()





        except ValueError:
            engine.say("No se ha reconocido nigun numero")
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

