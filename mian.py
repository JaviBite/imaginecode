#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import json
import Boxes

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from word2number import w2n

import speaker as s
#import recognition as sr
import recognition as srr
import speech_recognition as sr
# obtain audio from the microphone
#r = sr.Recognizer()

r = sr.Recognizer()

WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings
WIT_AI_KEY_ES = "IECUWB7JXYTAFP4NB25DCM5NFD7TCP4M"





s.speack("Hi I am your voice assistant")

# engine.say("Hi i am your voice assistant")
# engine.runAndWait()

# Detecta el color de la frase
def color_voice(voice_text):
    for color in Boxes.boxes:
        if color in voice_text:
            return color
    return None

# Detecta el item en cont del voice_text
def searchfor_item(cont, voice):
    for box in cont:
        for item in box["items"]:
             if item["name"] in voice:
                 return item["name"]
    return "NONE"

# Detecta el box de cont del voice_text
def searchfor_box(cont, voice):
    for box in cont:
         if box["name"] in voice:
             return box["name"]
    return "NONE"

# Devuelve la orden de dejar el objeto en un contenedor destion apto
#
# number = objetos en mano
# cont_o = de donde los ha cogido
# name_d = nombre objeto en la mano
# cont_d = lista cont destino
def orderDrop(cont_d, name_d, number, cont_o, to_drop):
    for box in cont_d:
        for item in box["items"]:
            if item["name"] == name_d and item["n"] != 0:
                if item["n"] >= number:
                    #item["n"] = item["n"] - number
                    to_drop[0] = box["name"]
                    return "Put " + str(number) + " " + item["name"] + " into the " + box["name"] + " box"
                else:
                    #aDev = "Put " + str(item["n"] - ) + " " + item["name"] + " into the " + box["name"] \
                    #       + " box and leave the rest one at the origin " + cont_o["name"]
                    #item["n"] = 0
                    return "Put " + str(number) + " " + item["name"] + " back"

    return "There are not " + str(number) + " " + item["name"] + " into the " + box["name"] + " box"

# modifica el contenedor cont_name de la lista cont los objetos item_name + n
def modify(cont,cont_name,num,item_name):
    for box in cont:
        if box["name"] == cont_name:
            for item in box["items"]:
                if item["name"] == item_name:
                    item["n"] = item["n"] + num

def orderPick(cont_d, cont_o, to_pick, to_number):
    for box in cont_d:
        for item in box["items"]:
            num = item["n"]
            if num > 0:
                box_to_search = box["name"]
                to_pick[0] = box_to_search
                to_number[0] = num
                if box_to_search != "NONE":
                    return "Pick up " + str(num) + " " + item["name"] + ("s" if num > 1 else "") + \
                           " from origin box " + box["name"]
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

item_inHands = None
num_inHands = 0
to_drop = [1]
to_drop[0] = None
to_pick = [1]
to_pick[0] = None
to_number = [1]
to_number[0] = 0

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    while not ordenTerminada:

        ord = orderPick(cont_d, cont_o, to_pick, to_number) if item_inHands is None else \
            orderDrop(cont_d, item_inHands, num_inHands, cont_o, to_drop)

        s.speack(ord)
        print("Order: " + ord + "\n")
        print("Say something!")

        #Escuchar
        #audio = r.listen(source)

        try:
            audio = r.listen(source)
            voice_text = r.recognize_wit(audio, key=WIT_AI_KEY_ES)
            #voice_text = sr.recognice()
            #voice_text = "pick up three glass from origin box blue"
            # print("escibe: ")
            # voice_text = input()
            number = srr.numbers(voice_text)

            print("Usuario ha dicho: " + voice_text)
            print("Numero transcrito: " + str(number))

            if ("repeat" in voice_text or ("dont" in voice_text and "understand" in voice_text)):
                # s.speack(ord)
                print("Repetir orden")
            elif ("okey" in voice_text or "done" in voice_text ):
                print("TODO")
            elif (" d " in voice_text):
                if ("drop" in voice_text):
                    box = color_voice(voice_text)
                    if box == None:
                        box = to_drop
                    item_inHands = searchfor_item(cont_d,voice_text)
                    modify(cont_d,box,-num_inHands,item_inHands)
                    item_inHands = None
                    num_inHands = 0

                elif "pick" in voice_text:
                    box = color_voice(voice_text)
                    if box == None:
                        box = to_pick
                    item_inHands = searchfor_item(cont_d, voice_text)
                    num_inHands = number
                    modify(cont_d, box,+num_inHands, item_inHands)

            elif (" o " in voice_text):
                if ("drop" in voice_text):
                    box = color_voice(voice_text)
                    if box == None:
                        box = to_drop
                    item_inHands = searchfor_item(cont_o, voice_text)
                    modify(cont_o, box, +num_inHands, item_inHands)
                    item_inHands = None
                    num_inHands = 0

                elif ("pick" in voice_text):
                    box = color_voice(voice_text)
                    if box == None:
                        box = to_pick
                    num_inHands = number
                    item_inHands = searchfor_item(cont_o, voice_text)
                    modify(cont_o, box, -num_inHands, item_inHands)

                # ordDest = "none"
                #
                # for box in cont_o:
                #     for item in box["items"]:
                #         if item["name"] in voice_text:
                #             ordDest = orderDest(cont_d, item["name"], number, box["name"])
                #             # ordenTerminada = True
                #
                # while ("okey" not in voice_text):
                #     s.speack(ordDest)
                #     print("Ord2: " + ordDest + "\n")
                #     # Tratar respuesta
                #     voice_text = sr.recognice()


        except ValueError:
            s.speack("I didnt recognize any number")
            print("Usuario ha dicho: " + voice_text)
        except sr.UnknownValueError:
            s.speack("Sorry, I didnt understand you phrase")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
            s.speack("Sorry, I cant connect to my system")

