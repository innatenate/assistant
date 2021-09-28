
#imports
import speech_recognition as sr
import sounddevice as sd
import pyttsx3
import numpy as np
import pyaudio
import time
import keywordprocessor
import traceback
import universal
import errorhandler


#variables
hot = False
processed = False
users = ['Nate']
currentUser = users[0]


#init
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
sd.default.samplerate = 48000
recognizer = sr.Recognizer()
previousStrings = []
rating = 0
sensitivity = 10                                         ## ADJUST SENSITIVITY
average = 0
started = None

def detect_sound(indata, odate, frames, time, status):
    global average
    global rating                               ## SOUND DETECTION
    volume = np.linalg.norm(indata)*5
    string = ("-" * int(volume))
    if string not in previousStrings:
        previousStrings.insert(0, string)
    if len(previousStrings) > 10:
        previousStrings.pop((len(previousStrings)-1))
    average = 0
    for string in previousStrings:
        average += len(string)
    average = average/len(previousStrings)
    rating = average + sensitivity
    if len(string) > rating:
        global hot
        global processed
        processed = False
        hot = True


while 1:
    while not hot:
        with sd.Stream(callback=detect_sound):
            sd.sleep(1500)
    while hot:
        if processed and hot:
            hot = False
        else:
            try:
                print("[PROC] Attempting to listen")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout = 2)
                    text = recognizer.recognize_google(audio, language="en-US")
                    if len(text) > 0:
                        status = keywordprocessor.Process(text)
                        if not status:
                            print(f"error: {text}")
                        hot = False
                        processed = True
                    else:
                        print(f"error: {text}")

            except Exception as ex:
                hot = False
                processed = False
                if not ex.__class__.__name__ == "TimeoutError" and not ex.__class__.__name__ == "WaitTimeoutError":
                    info = ["1", repr(ex), traceback.print_tb(ex.__traceback__)]
                    errorhandler.report(info)

                                                                                          ## ERROR HANDLER






