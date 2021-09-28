import boto3
from pygame import mixer
import time
import os
import universal

polly = boto3.Session(
    aws_access_key_id="AKIAW62R2AZRJ32TRXFJ",
    aws_secret_access_key="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",
    region_name="us-east-1").client('polly')

mixer.init()

spoken = 0

def process(speak, ssml=False, client = False):
    global spoken
    spoken += 1
    try:
        if ssml:
            response = polly.synthesize_speech(VoiceId="Matthew",
                                               OutputFormat="mp3",
                                               Text=speak,
                                               TextType="ssml",
                                               Engine='neural')
        else:
            response = polly.synthesize_speech(VoiceId="Matthew",
                                               OutputFormat="mp3",
                                               Text=speak,
                                               Engine='neural')
    except Exception as e:
        if e.__traceback__:
            print(repr(e.__traceback__))
        try:
            response = polly.synthesize_speech(VoiceId="Matthew",
                                               OutputFormat="mp3",
                                               Text=speak,
                                               Engine='standard')
        except Exception:
            raise Exception("Unsuccessful text to speech process")
            return False
    file = open(f"speech{spoken}.mp3", 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    mixer.music.unload()
    mixer.music.load(f"speech{spoken}.mp3")
    if not client:
        mixer.music.play()
        while mixer.music.get_busy():
            if os.path.exists(f"speech{spoken-1}.mp3"):
                os.remove(f"speech{spoken-1}.mp3")
    else:
        universal.speech = spoken
