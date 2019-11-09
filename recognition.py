import speech_recognition as sr
from word2number import w2n

r = sr.Recognizer()

WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings
WIT_AI_KEY_ES = "IECUWB7JXYTAFP4NB25DCM5NFD7TCP4M"


def recognice():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        return r.recognize_wit(audio, key=WIT_AI_KEY)

def numbers(text):
    return w2n.word_to_num(text)
