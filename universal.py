#imports
import sounddevice as sd
import pyttsx3
import speechhandle
import commandprocessor
import errorhandler
import speech_recognition as sr
import sounddevice as sd
import traceback
import keywordprocessor
import pyaudio
import time
import requests


#init
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
sd.default.samplerate = 48000
lastPhrase = ""
pastPhrases = []
alertBank = []
currentQueries = []
waitingForQuery = False
recognizer = sr.Recognizer()
context = []
speech = 0

currentWeather = None
hourWeather = None

#   query object
#         TYPE: YESNO SPECIFIC
#         KEYWORDS: ""
#         PROCESS: FUNCTION

def speak(phrase, ssml=False, client=False):
    if ssml:
        phrase = "<speak>" + phrase + "</speak>"
    speechhandle.process(phrase, ssml, client)
    global lastPhrase
    lastPhrase = phrase
    global pastPhrases
    pastPhrases.insert(0, phrase)
    if len(pastPhrases) > 5:
        pastPhrases.pop(5)


def query(selectedQuery):
    global currentQueries
    global waitingForQuery

    if selectedQuery not in currentQueries:
        currentQueries.insert(0, selectedQuery)
        waitingForQuery = True
        status = False
        while not status:
            try:
                print("[PROC] Attempting to listen")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio, language="en-US")
                    status = keywordprocessor.Process(text)
                    if not status:
                        print(f"error: {text}")
            except Exception:
                speak(commandprocessor.selectandspeak(["I didn't process that correctly. Let's try again.", "Something didn't seem write with that response. Let's try again.", "I don't think that's a valid response. I said "]))
                speak(pastPhrases[1])
            time.sleep(0.2)
    else:
        return Exception

def contextulizer(parameter, method="add", contextType=list):
    """methods:
    literal check: checks for the exact object, works for strings or ints
    check: operationally checks object, good for checking for lists
    remove: remove an object from context
    add: default method, adds to context and removes rife context"""

    global context

    print(f"\n [CONT] Contextualizer contextualizing context:\nparameter:    {str(parameter)}\nmethod:   {method}\n")
    print(f"[CONT] Current context contextualized by contextualizer: {str(context)}")

    if method == "literalcheck":
        if parameter in context:
            return context
        else:
            return False

    if method == "check":
        for text in context:
            if type(text) == contextType:
                if type(text) == list and parameter in text:
                    return text
                elif parameter == text:
                    return text

        return False

    if method == "remove":
        context.remove(context.index(parameter))

    if method == "add":
        if len(context) >= 5:
            context.remove(len(context))
        context.insert(0, parameter)
        print(f"[SUCC] Contextualizer complete contextualization of \n    {str(context)}\n           type: {type(context)}")
        return context





####        askedpressurechanges        high    low
####        askedweathertrend            poor    fair    good    windy