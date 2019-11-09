#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import json
import Boxes

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from word2number import w2n

import speaker as s
import recognition as sr
# obtain audio from the microphone
#r = sr.Recognizer()

s.speack("Hi I am your voice assistant")

# engine.say("Hi i am your voice assistant")
# engine.runAndWait()

# Detecta el color de la caja
def contains_color(voice_text):
    for color in Boxes:
        if color in voice_text:
            return color


# El color de la caja de destino será el detectado
def Search(voice_text, cont_d):
    if "destiny" in voice_text:
        for box in cont_d:
            color = contains_color(voice_text)


def searchfor(cont, item_to):
    for box in cont:
        for item in box["items"]:
             if item["name"] == item_to:
                 return box["name"]
    return "NONE"

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

def order(cont_d, cont_o):
    for box in cont_d:
        for item in box["items"]:
            num = item["n"]
            if num > 0:
                box_to_search = searchfor(cont_o, item["name"])
                if box_to_search != "NONE":
                    return "Pick up " + str(num) + " " + item["name"] + ("s" if num > 1 else "") + \
                           " from origin box " + box_to_search
                else:
                    return "The task cant be completed"

    return "You have finished your task"


# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source)

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


ordenTerminada = False
while not ordenTerminada:

    #Mandar orden
    ord = order(cont_d, cont_o)
    s.speack(ord)
    print(ord + "\n")
    print("Say something!")



    #Escuchar
    #audio = r.listen(source)

    try:
        #voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)
        voice_text = sr.recognice()
        number = sr.numbers(voice_text)

        print("Usuario ha dicho: " + voice_text)
        print("Numero transcrito: " + str(number))

        if "repeat" in voice_text or ("dont" in voice_text and "understand" in voice_text):
            # s.speack(ord)
            print("Repetir orden")
        elif ("okey" in voice_text):
            print("TODO")
        elif ("pick" in voice_text):

            ordDest = "none"

            for box in cont_o:
                for item in box["items"]:
                    if item["name"] in voice_text:
                        ordDest = orderDest(cont_d, item["name"], number, box["name"])
                        # ordenTerminada = True

            while ("okey" not in voice_text):
                s.speack(ordDest)
                print("Ord2: " + ordDest + "\n")
                # Tratar respuesta
                voice_text = sr.recognice()



    except ValueError:
        s.speack("I didnt recognize any number")
        print("Usuario ha dicho: " + voice_text)
    except sr.sr.UnknownValueError:
        s.speack("Sorry, I didnt understand you phrase")
    except sr.sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
        s.speack("Sorry, I cant connect to my system")

