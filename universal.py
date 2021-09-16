#imports
import sounddevice as sd
import pyttsx3
import errorhandler
import speech_recognition as sr
import sounddevice as sd
import traceback
import keywordprocessor
import pyaudio

#init
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
sd.default.samplerate = 48000
lastPhrase = ""
alertBank = []
currentQueries = []
waitingForQuery = False
recognizer = sr.Recognizer()

#   query object
#         TYPE: YESNO SPECIFIC
#         KEYWORDS: ""
#         PROCESS: FUNCTION

def query(selectedQuery):
    global currentQueries
    global waitingForQuery
    if selectedQuery not in currentQueries:
        currentQueries.insert(0, selectedQuery)
        print(currentQueries[0])
        waitingForQuery = True
        print("done installing query, now commencing listening")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="en-US")
                print("Processed text to " + str(text))
                status = keywordprocessor.Process(text)
        except Exception as ex:
            info = ["1", repr(ex), traceback.print_tb(ex.__traceback__)]
            errorhandler.report(info)
            hot = False
    else:
        print('problem chief')
        return Exception



def speak(phrase) -> object:
    print(phrase)
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()
    global lastPhrase
    lastPhrase = phrase

