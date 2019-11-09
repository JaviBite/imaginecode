#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import json
import Boxes
import languages as l

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

class ExpImposible(BaseException):
    msg = "error"

r = sr.Recognizer()

debug = False
language = "es"

s.setLanguage(language)

WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN" if language == "en" else "IECUWB7JXYTAFP4NB25DCM5NFD7TCP4M"

lan = l.en if language == "en" else l.es

# return s or es for plurals
def plural(item):

    if item[-1:] == 's' or item[-1:] == 'l' or item[-1:] == 'n':
        return "es"
    else:
        return "s"

# Detecta el item en cont del voice_text
def searchfor_item(cont, voice):
    for box in cont:
        for item in box["items"]:
             if item["name"] in voice:
                 return item["name"]
    return "NONE"

# Detecta el box de cont del voice_text
def searchbox_from_item(cont, item_s):
    for box in cont:
        for item in box["items"]:
            if item["name"] in item_s:
                return box["name"]
    return "NONE"

# Detecta el box de cont del voice_text
def searchfor_box(cont, voice):
    for box in cont:
         if str(box["name"]) in voice:
             return str(box["name"])
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
                    to_drop[0] = str(box["name"])
                    return lan.drop + " " + str(number) + " " + item["name"] + (plural(item["name"]) if number > 1 else "") + \
                           lan.into_d + str(box["name"]) + " " + lan.bx
                else:
                    #aDev = "Put " + str(item["n"] - ) + " " + item["name"] + " into the " + str(box["name"]) \
                    #       + " box and leave the rest one at the origin " + cont_o["name"]
                    #item["n"] = 0
                    return lan.drop + str(number) + " " + item["name"] + lan.back

    raise Exception

# modifica el contenedor cont_name de la lista cont los objetos item_name + n
def modify(cont,cont_name,num,item_name):
    for box in cont:
        if box["name"] == cont_name:
            for item in box["items"]:
                if item["name"] == item_name:
                    item["n"] = item["n"] + num
                    return None
    raise ExpImposible


def orderPick(cont_d, cont_o, to_pick, to_number):
    for box in cont_d:
        for item in box["items"]:
            num = item["n"]
            if num > 0:
                box_to_search = searchbox_from_item(cont_o, item["name"])
                to_pick[0] = box_to_search
                to_number[0] = num
                if box_to_search != "NONE":
                    return lan.pick + " " + str(num) + " " + item["name"] + (plural(item["name"]) if num > 1 else "") + \
                           lan.from_o + " " + str(box_to_search)
                else:
                    return lan.task_cant

    return lan.task_end


    # leer archivo

with open('fichero_4_2.json') as json_file:
    data = json.load(json_file)

cont_o = data["origin"]
cont_d = data["destiny"]

ordenTerminada = False

item_inHands = None
num_inHands = 0
to_drop = [1]
to_drop[0] = None
to_pick = [1]
to_pick[0] = None
to_number = [1]
to_number[0] = 0

s.speack(lan.hola)

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    while not ordenTerminada:

        ord = orderPick(cont_d, cont_o, to_pick, to_number) if item_inHands is None else \
            orderDrop(cont_d, item_inHands, num_inHands, cont_o, to_drop)

        print("Order: " + ord + "\n")

        i = searchfor_item(cont_o,ord)

        if " 1 " in ord:
            if i[-1:] == 'a':
                ord = ord.replace(" 1 ", " una ")
            else:
                ord = ord.replace(" 1 ", " un ")

        s.speack(ord)

        #Escuchar
        #audio = r.listen(source)

        try:

            if debug:
                print("escribe: ")
                voice_text = input()
            else:
                print("Say something!")
                audio = r.listen(source)
                voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)
                voice_text = voice_text.replace('dejó','dejo')
                voice_text = voice_text.replace('tulipán', 'tulipan')

            if (lan.end in voice_text):
                print(lan.pause)
                s.speack(lan.pause)
                voice_text = ""
                while lan.res not in voice_text:
                    audio = r.listen(source)
                    voice_text = r.recognize_wit(audio, key=WIT_AI_KEY)
                s.speack(lan.resume)
            elif (lan.rpt in voice_text or (lan.unders in voice_text)):
                # s.speack(ord)
                print("Repetir orden")

            if lan.orig in voice_text:
                before_box = voice_text[0:voice_text.index(lan.orig)]
                after_box = voice_text[voice_text.index(lan.orig):]
            else:
                before_box = voice_text[0:voice_text.index(lan.dest)]
                after_box = voice_text[voice_text.index(lan.dest):]

            if language == 'es':
                number = Boxes.toNum(before_box) #srr.numbers(voice_text)
                box_number = Boxes.toNum(after_box) #srr.numbers(voice_text)
            else:
                number = srr.numbers(before_box)
                box_number = srr.numbers(after_box)

            print(lan.creo + voice_text)
            print("Item num: " + str(number)+ " Box: " + str(box_number))


            if (lan.dest in voice_text):
                if (lan.to_drop in voice_text):
                    box = box_number
                    if box == None:
                        box = to_drop
                    item_inHands_aux = searchfor_item(cont_d,voice_text)
                    modify(cont_d, box, -num_inHands_aux, item_inHands_aux)
                    item_inHands = None
                    num_inHands = 0

                elif lan.to_pick in voice_text:
                    box = box_number
                    if box == None:
                        box = to_pick
                    item_inHands_aux = searchfor_item(cont_d, voice_text)
                    num_inHands_aux = number
                    modify(cont_d, box,+num_inHands_aux, item_inHands_aux)
                    num_inHands = num_inHands_aux
                    item_inHands = item_inHands_aux

            elif (lan.orig in voice_text):
                if (lan.to_drop in voice_text):
                    box = box_number
                    if box == None:
                        box = to_drop
                    item_inHands_aux = searchfor_item(cont_o, voice_text)
                    modify(cont_o, box, +num_inHands_aux, item_inHands_aux)
                    item_inHands = None
                    num_inHands = 0

                elif (lan.to_pick in voice_text):
                    box = box_number
                    if box == None:
                        box = to_pick
                    num_inHands_aux = number
                    item_inHands_aux = searchfor_item(cont_o, voice_text)
                    modify(cont_o, box, -num_inHands_aux, item_inHands_aux)
                    num_inHands = num_inHands_aux
                    item_inHands = item_inHands_aux

        except ExpImposible:
            s.speack(lan.imposible)
            print("Accion imposible, vuelve al estado anterior")
        except ValueError as e:
            s.speack(lan.problema)
            print(lan.creo + voice_text)
        except sr.UnknownValueError:
            s.speack(lan.srry)
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
            s.speack(lan.connex)
        except Exception:
            s.speack(lan.problema)
            print(lan.creo + voice_text)


