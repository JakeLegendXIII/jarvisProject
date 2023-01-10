import os
import sys
import subprocess
from tempfile import gettempdir
from contextlib import closing
import openai as ai
import pyaudio
import speech_recognition as sr
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from pydub import AudioSegment
from pydub.playback import play

ai.organization = os.environ.get('API_ORG')
ai.api_key = os.environ.get('API_KEY')


def query_ai(prompt):
    print('Prompt:', prompt)
    completions = ai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].text
    print('Message: ', message)
    return message


def listen_for_wake_word():
    r = sr.Recognizer()
    print('Accessing Microphone')
    with sr.Microphone(0) as source:
        print('Listening for Wake Word')
        audio = r.listen(source, 10, 3)
        try:
            speech = r.recognize_google(audio)
            print(speech)
            if "hey jarvis" in speech.lower():
                print('wake word detected')
                audio_cmd = r.listen(source, 5, 15)
                cmd = r.recognize_google(audio_cmd)
                print('Command:', cmd)
                response = query_ai(cmd)
                speak(response)
            else:
                print('wake word not detected')
        except sr.RequestError:
            print('Request Error')
        except sr.UnknownValueError:
            print('UnknownValueError: Could not hear you')
        except sr.WaitTimeoutError:
            print('Wait Timeout Error: You took too long!')
    return

def speak(content):
    session = Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        region_name='us-east-2'
    )
    polly = session.client('polly')
    speech = polly.synthesize_speech(
        Text=content,
        OutputFormat='mp3',
        VoiceId='Brian'
    )
    audio = speech['AudioStream'].read()
    print('creating mp3 file')
    filename = 'jarvis.mp3'
    with open(filename, 'wb') as file:
        file.write(audio)
        file.close()
    clip = AudioSegment.from_mp3(filename)
    play(clip)

if __name__ == '__main__':
    # speak(query_ai('How long would it take to get to Mars?'))
    while True:
        listen_for_wake_word()
    print('It Works!')
