import speech_recognition as sr
import pyttsx3
import os
from playsound import playsound
import urllib.request
import webbrowser as web
#py audio should be installed alongside SR but is not sometimes and we went through a thing to get it in, install pipwin and then pyaudio




text= '-1'
def Core_Loop():
    r = sr.Recognizer()
    print('Speak')
    while True:

        with sr.Microphone() as source:

            audio = r.listen(source, phrase_time_limit=3.0)


            try:
                text = r.recognize_google(audio)
                text=text.lower()
                print(text)
                if 'abort' in text:
                    break
                elif 'computer shutdown' in text:
                    playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\oyasumi.wav')
                    shutdown()

                elif 'go to youtube' in text:
                         playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
                         audio = r.listen(source, phrase_time_limit=2.0)
                         text = r.recognize_google(audio)
                         text=text.lower()
                         print(text)
                         web.open_new(f'https://www.youtube.com/results?search_query={text}')

                else:
                    r = sr.Recognizer()
               
            except sr.UnknownValueError:
                r = sr.Recognizer()
                print('Audio not recognized Retrying..')

def shutdown():
    os.system('shutdown -s')
    




Core_Loop()

