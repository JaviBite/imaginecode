import pyttsx3

engine = pyttsx3.init()
engine.setProperty('volume', 10.0)

v_en = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
v_es = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

engine.setProperty('rate', 115)
engine.setProperty('voice', v_en)

def speack(string):
    engine.say(string)
    engine.runAndWait()
