#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# Import the required module for text
# to speech conversion
from gtts import gTTS

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        WIT_AI_KEY = "Y3FGBAGFPLAM5FU2LIO6WM6EBAZU3AHN"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

