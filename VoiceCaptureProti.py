import speech_recognition as sr
import os
import time
from playsound import playsound
import webbrowser as web
import urllib.request
import re
from datetime import datetime
import pyautogui as auto
from selenium import webdriver

################################################################
#ISSUES AND NEEDS SECTION

#create activation keyword
#create dict of responses #NOT A DICT SQL DATABSE BECAUSE WE CAN UPDATE IT LIVE KEKW
#voice repsonse
#Translator implementation
#implent GPTREQUEST
#playsound is fucked needs local path
#need to be able to choose default web browser
#Enable choice of videos of youtube.
###### ISSUES ##########

#py audio should be installed alongside SR but is not sometimes and we went through a thing to get it in, install pipwin and then pyaudio

#TODO Name it peresephone and add timestamps to notes

################################################################
#GLOBALS
rec = sr.Recognizer()
text= '-1'   
script_dir = os.path.dirname(os.path.abspath(__file__))
sound_path = os.path.join(script_dir, 'assets', 'Sounds', 'processing.mp3')
welcome_Sound = os.path.join(script_dir, 'assets', 'Sounds', 'GLaDOS_Aperture_labs_helping_you_help_u.wav')


################################################################
#Calibration
#Calibration was pointless?
#with sr.Microphone() as source:   
     #print("Please wait. Calibrating microphone...")
     #playsound(welcome_Sound)   
     # listen for 5 seconds and calculate the ambient noise energy level   
     #rec.adjust_for_ambient_noise(source, duration=3)
     #rec.dynamic_energy_threshold = True
    
     
################################
def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
if __name__ == "__main__":
    main()

            

################################################################
#Command Loop
def Core_Loop():
    print('Speak')
    while True:
        try:
            with sr.Microphone() as source:
                    audio = rec.listen(source, phrase_time_limit=3.0)
                    print(f'waiting for Listen Command')
                    text = rec.recognize_google(audio).lower()
                    print(text)
                    if 'listen' in text:
                        print('Now listening')
                        secondary_Loop()
                        break
        except sr.UnknownValueError:
            sr.Recognizer()
            print('...')

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
                elif 'close tab' in text:
                    print('tab close')
                    clost_Tab()
                elif 'take notes' in text:
                    take_Notes()
                elif 'go to youtube' in text:
                    print(sound_path)
                    playsound(sound_path)
                    go2youtube()  
                elif 'google something for me' in text:
                    go2google()
                elif 'open chat' in text:
                    go2Gpt()    
                elif 'pause' in text:
                    keystroke()
                else:
                    print('restarting Command loop')
                    secondary_Loop()
            
            except sr.UnknownValueError:
                sr.Recognizer()
                print('....Breaking Command Loop?')




########################################################################
#Functions
def keystroke():
    print('Executing')
    auto.press('space')

def shutdown():
    print('Executing')
    os.system('shutdown -s')
def clost_Tab():
    auto.hotkey('ctrl', 'w')
def take_Notes():
    complete_note = ''
    looping = True
    while looping == True:
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=10.0)
            text = rec.recognize_google(audio).lower()
            print(text)
            complete_note += text    
            print('note_text: ', text)
        if "stop listening" in text:
                print("Stop command detected. Exiting loop.")
                break

    current_timestamp = datetime.now()
    try:
        with open ('example.txt', 'a') as file:
            file.write(f'\n---{current_timestamp}---{complete_note}')
            print('Wrote to file')
    except:
        print('failure to write')
    
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
       #TODO we need to webscrap our way to the selection with selenium, hotkeys and tab method proved cumbersome. 

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

##############################################################
#RunTime

Core_Loop()


