import speech_recognition as sr
import os
from playsound import playsound
import webbrowser as web
import urllib.request
import re
#py audio should be installed alongside SR but is not sometimes and we went through a thing to get it in, install pipwin and then pyaudio


text= '-1'

def Core_Loop():
    r = sr.Recognizer()
    print('Speak')
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=3.0)
            try:
                text = r.recognize_google(audio).lower()
                print(text)
                if 'abort' in text:
                    break
                elif 'computer shutdown' in text:
                    playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\oyasumi.wav')
                    shutdown()
                elif '3030' in text:
                    os.system("taskkill /im vivaldi.exe /f")
                elif 'go to youtube' in text:
                    go2youtube()
                else:
                    r = sr.Recognizer()
               
            except sr.UnknownValueError:
                r = sr.Recognizer()
                print('..')

def shutdown():
    os.system('shutdown -s')
def go2youtube():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
        audio = r.listen(source, phrase_time_limit=2.0)
        text = r.recognize_google(audio).lower().replace(' ','+' )
        print(text)
        html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={text}')
        videoids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        #print(videoids)
        #youtube apparently did not put these in order as i get repeats and missing sequentials here, prolly parse is bad

        #we fail to close this after selection is picked
        web.open_new(f'https://www.youtube.com/results?search_query={text}')

        audio = r.listen(source, phrase_time_limit=2.0)
        text = r.recognize_google(audio).lower()
        print(text)
        if 'first one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v= {videoids[0]}')
        elif 'second one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v={videoids[1]}')
        elif 'third one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v={videoids[2]}')
                            

#RunTime

Core_Loop()

