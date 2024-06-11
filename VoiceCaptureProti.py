import speech_recognition as sr
import os
import time
from playsound import playsound
import webbrowser as web
import urllib.request
import re
import pyautogui as auto
from selenium import webdriver

################################################################
#ISSUES AND NEEDS SECTION

#create activation keyword
#create dict of responses
#voice repsonse
#Translator implementation
#implent GPTREQUEST
#playsound is fucked needs local path
#need to be able to choose default web browser
#Enable choice of videos of youtube.
###### ISSUES ##########

#py audio should be installed alongside SR but is not sometimes and we went through a thing to get it in, install pipwin and then pyaudio



################################################################
#GLOBALS
rec = sr.Recognizer()
text= '-1'
script_dir = os.path.dirname(os.path.abspath(__file__))
sound_path = os.path.join(script_dir, 'assets', 'oyasumi.wav')

################################################################
#Command Loop
def Core_Loop():
    print('Speak')
    while True:
        try:
            with sr.Microphone() as source:
                    audio = rec.listen(source, phrase_time_limit=3.0)
                    print('not listening')
                    text = rec.recognize_google(audio).lower()
                    print(text)
                    if 'start listening' in text:
                        secondary_Loop()
                        break
        except sr.UnknownValueError:
            sr.Recognizer()
            print('?')

def secondary_Loop():
     while True:
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=3.0)
            text = rec.recognize_google(audio).lower()
            print(text)
            try:
                if '11:11' in text:
                    Core_Loop()
                    break
                elif 'we are done' in text:
                    playsound(sound_path)
                    shutdown()
                elif '3030' in text:
                    #very specific :(
                    os.system("taskkill /im vivaldi.exe /f")
                elif 'go to youtube' in text:
                    print(sound_path)
                    playsound(sound_path)
                    go2youtube()  
                elif 'google something for me' in text:
                    go2google()
                elif 'internet this' in text:
                    internet4me()
                    #This is preserved for a youtube function but we are debating screen toggles and whether it is worth it. 
                elif 'open chat' in text:
                    go2Gpt()    
                elif 'pause' in text:
                    keystroke()
                else:
                    sr.Recognizer()
            
            except sr.UnknownValueError:
                sr.Recognizer()
                print('....?')




########################################################################
#Functions
def keystroke():
    print('Executing')
    auto.press('space')

def shutdown():
    print('Executing')
    os.system('shutdown -s')


#
def go2youtube():
    print('Executing')
    with sr.Microphone() as source:
        audio = rec.listen(source, phrase_time_limit=2.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        print(text)
        html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={text}')
        videoids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

        #we fail to close this after selection is picked
        web.open_new(f'https://www.youtube.com/results?search_query={text}')
        audio = rec.listen(source, phrase_time_limit=2.0)
        text = rec.recognize_google(audio).lower()
        print(text)
        if 'first one' in text:
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('tab')
            auto.press('enter')
            time.sleep(1)
            auto.press('enter')
            time.sleep(1)
            auto.press('left')

       

#worked as of 6/8/24 with default browser
def go2google():
    print('Executing')
    with sr.Microphone() as source:
        audio = rec.listen(source, phrase_time_limit=10.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        web.open_new(f'https://www.google.com/search?q={text}')

def go2Gpt():
        print('Executing')
        web.open_new(f'https://chatgpt.com')
        time.sleep(.5)
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=5.0)
            input_Text = rec.recognize_google(audio).lower()
            auto.typewrite(f'{input_Text}', interval=0.1)
            auto.hotkey('ctrl', 'enter')
            chatting = True
            print('chatting')
            while chatting == True:
                with sr.Microphone() as source:
                    audio = rec.listen(source, phrase_time_limit=5.0)
                    input_Text = rec.recognize_google(audio).lower()
                    if 'im done talking' in input_Text:
                        break
                    else:
                        auto.typewrite(f'{input_Text}', interval=0.1)
                        auto.hotkey('ctrl', 'enter')

#forgot what this is or why        
def internet4me():
        print('Executing')
        playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\input.mp3')
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=2.0)
            text = rec.recognize_google(audio).lower()


            #selenium dcriver is a fucking pain compared to webrowser BUT ILL FIGURE IT THE FUCK OUTblank
            driver = webdriver.Firefox()
            driver.get("https://www.python.org")
            
##############################################################
#RunTime

Core_Loop()


