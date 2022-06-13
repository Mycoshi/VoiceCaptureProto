import speech_recognition as sr
import os
from playsound import playsound
import webbrowser as web
import urllib.request
import re
import pyautogui as auto
from selenium import webdriver
#py audio should be installed alongside SR but is not sometimes and we went through a thing to get it in, install pipwin and then pyaudio

rec = sr.Recognizer()
text= '-1'
#Command Loop
def Core_Loop():
    print('Speak')
    while True:
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=3.0)
            try:
                text = rec.recognize_google(audio).lower()
                print(text)
                if 'abort' in text:
                    breakblank
                elif 'we are done' in text:
                    playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\oyasumi.wav')
                    shutdown()
                elif '3030' in text:
                    #very specific :(
                    os.system("taskkill /im vivaldi.exe /f")
                elif 'go to youtube' in text:
                    go2youtube()
                
                elif 'google something for me' in text:
                    go2google()
                elif 'internet this' in text:
                    internet4me()
                    #This is preserved for a youtube function but we are debating screen toggles and whether it is worth it. 
                elif 'pause' in text:
                    keystroke()
                else:
                    sr.Recognizer()
               
            except sr.UnknownValueError:
                sr.Recognizer()
                print('..')


def keystroke():
    auto.press('space')



def shutdown():
    os.system('shutdown -s')

def go2youtube():
    with sr.Microphone() as source:
        playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
        audio = rec.listen(source, phrase_time_limit=2.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        print(text)
        html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={text}')
        videoids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        #print(videoids)
        #youtube apparently did not put these in order as i get repeats and missing sequentials here, prolly parse is bad

        #we fail to close this after selection is picked
        web.open_new(f'https://www.youtube.com/results?search_query={text}')
        audio = rec.listen(source, phrase_time_limit=2.0)
        text = rec.recognize_google(audio).lower()
        print(text)
        #THOT IT WAS KINDA FUCKED IT WAS KINDA REALLY FUCKED
        if 'first one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v= {videoids[0]}')
        elif 'second one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v={videoids[1]}')
        elif 'third one' in text:
            web.open_new(f'https://www.youtube.com/watch\?v={videoids[2]}')

#v2 is so much slower maybe thats firefoxes fault? but i doubt it
# def go2youtubev2():
#     with sr.Microphone() as source:
#         playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
#         audio = rec.listen(source, phrase_time_limit=2.0)
#         text = rec.recognize_google(audio).lower().replace(' ','+' )
#         print(text)
#         driver = webdriver.Firefox()
#         driver.get(f"https://www.youtube.com/results?search_query={text}")
#         driver.maximize_window()



#         html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={text}')
#         videoids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
#         audio = rec.listen(source, phrase_time_limit=5.0)
#         text = rec.recognize_google(audio).lower()
#         print(text)
#         if 'first one' in text:
#                driver.get(f'https://www.youtube.com/watch\?v= {videoids[0]}')
#         elif 'second one' in text:
#                driver.get(f'https://www.youtube.com/watch\?v={videoids[1]}')
#         elif 'third one' in text:
#                driver.get(f'https://www.youtube.com/watch\?v={videoids[2]}')
                            
def go2google():
    playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
    with sr.Microphone() as source:
        audio = rec.listen(source, phrase_time_limit=5.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        web.open_new(f'https://www.google.com/search?q={text}')
def internet4me():
        playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=2.0)
            text = rec.recognize_google(audio).lower()


            #selenium dcriver is a fucking pain compared to webrowser BUT ILL FIGURE IT THE FUCK OUTblank
            driver = webdriver.Firefox()
            driver.get("https://www.python.org")
            
    
#RunTime

Core_Loop()


