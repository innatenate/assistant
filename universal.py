#imports
import sounddevice as sd
import pyttsx3

import commandprocessor
import errorhandler
import speech_recognition as sr
import sounddevice as sd
import traceback
import keywordprocessor
import pyaudio
import time

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

#   query object
#         TYPE: YESNO SPECIFIC
#         KEYWORDS: ""
#         PROCESS: FUNCTION

def speak(phrase) -> object:
    print(phrase)
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()
    global lastPhrase
    lastPhrase = phrase
    global pastPhrases
    pastPhrases.insert(0, phrase)
    if len(pastPhrases) > 5:
        pastPhrases.remove(len(pastPhrases))

def query(selectedQuery):
    global currentQueries
    global waitingForQuery

    if selectedQuery not in currentQueries:
        currentQueries.insert(0, selectedQuery)
        print(currentQueries[0])
        waitingForQuery = True
        print("done installing query, now commencing listening")
        status = False
        while not status:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio, language="en-US")
                    print("Processed text to " + str(text))
                    status = keywordprocessor.Process(text)
            except Exception:
                speak(commandprocessor.selectandspeak(["I didn't process that correctly. Let's try again.", "Something didn't seem write with that response. Let's try again.", "I don't think that's a valid response. I said "]))
                speak(pastPhrases[1])
            time.sleep(0.2)
    else:
        print('problem chief')
        return Exception

def contextulizer(parameter, method="add", contextType=list):
    """methods:
    literal check: checks for the exact object, works for strings or ints
    check: operationally checks object, good for checking for lists
    remove: remove an object from context
    add: default method, adds to context and removes rife context"""

    global context

    print(f"\n Contextualizer contextualizing context:\nparameter:    {str(parameter)}\nmethod:   {method}\n")
    print(f"Current context contextualized by contextualizer: {str(context)}")

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
        print(f"Contextualizer complete contextualization of \n    {str(context)}\n           type: {type(context)}")
        return context





####        askedpressurechanges        high    low
####        askedweathertrend            poor    fair    good    windy