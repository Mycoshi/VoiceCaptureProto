import speech_recognition as sr
import os
import time
from playsound import playsound
import webbrowser as web
import urllib.request
import re
from datetime import datetime
import pyautogui as auto
import noisereduce as nr
import numpy as np
import pywinauto
import subprocess
import threading

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
url='-1'
Talking = False
talking_thread = None

sound_path = os.path.join(script_dir, 'assets', 'Sounds', 'processing.mp3')
welcome_Sound = os.path.join(script_dir, 'assets', 'Sounds', 'GLaDOS_Aperture_labs_helping_you_help_u.wav')


base_sound_path = os.path.join(script_dir, 'assets', 'Sounds')
for file in os.listdir(base_sound_path):
    full_path = os.path.join(base_sound_path, file)

################################################################
#Calibration
def preprocess_audio(audio_data):
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    cleaned_audio = nr.reduce_noise(y=audio_np, sr=16000)
    return cleaned_audio.tobytes()

# Function to recognize audio with preprocessing
def recognize_audio(recognizer, source):
    try:
        audio = recognizer.listen(source, timeout=7, phrase_time_limit=15)
        cleaned_audio = preprocess_audio(audio.get_raw_data())
        return recognizer.recognize_google(sr.AudioData(cleaned_audio, source.SAMPLE_RATE, source.SAMPLE_WIDTH)).lower()
    except sr.UnknownValueError:
        print("Unable to understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None
            

################################################################
#Command Loop
def Core_Loop():
    print('Speak')
    while True:
        try:
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=3.0)
                text = rec.recognize_google(audio).lower()
                print(text)
                
                # Check if the activation phrase is present in the recognized text
                if 'juno' in text or 'do you know' in text:
                    print('Juno Hears')
                    secondary_Loop()
                else:
                    print('Activation keyword not detected.')
        except sr.UnknownValueError:
            print('Unable to understand the audio.')
        except sr.RequestError as e:
            print(f'Error with the speech recognition service: {e}')

def secondary_Loop():
     playsound
     while True:
        try:
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=7.0)
                text = rec.recognize_google(audio).lower()
                print(text)

                if '11:11' in text:
                    Core_Loop()
                    break
                elif 'we are done' in text:
                    playsound(sound_path)
                    shutdown()
                elif "i'm talking" in text:
                    start_talking()
                elif "internet" in text:
                    focus_vivaldi()    
                elif '3030' in text:
                    os.system("taskkill /im vivaldi.exe /f")
                elif 'close tab' in text:
                    close_Tab()
                elif 'take notes' in text:
                    take_Notes()
                elif 'go to youtube' in text:
                    playsound(sound_path)
                    go2youtube()
                elif 'google something for me' in text:
                    go2google()
                elif 'open chat' in text or 'go to chat' in text:
                    go2Gpt()
                elif 'pause' in text:
                    keystroke()
                else:
                    print('Unknown command. Restarting loop.')

        except sr.UnknownValueError:
            print('Returning to Command Loop UnknownValueError.')
        except sr.RequestError as e:
            print(f'Error with the speech recognition service: {e}')

def start_talking():
    global Talking, talking_thread
    if Talking:
        print("Already talking.")
        return
    Talking = True
    talking_thread = threading.Thread(target=talk_thread)
    talking_thread.start()

def stop_talking():
    global Talking
    Talking = False
    if talking_thread:
        talking_thread.join()
    print("Stopped talking.")
    
def talk_thread():
   global Talking
   while Talking:
        try:
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=10.0)
                input_text = rec.recognize_google(audio).lower()
                if "i'm done" in input_text or 'quit' in input_text:
                    print("Stop talking.")
                    Talking = False
                else:
                    auto.typewrite(f'{input_text}', interval=0.1)
                    auto.hotkey('ctrl', 'enter')
        except Exception as e:
            print(f'Error during talking: {e}')
            start_talking()

def focus_vivaldi():
    try:
        # Attempt to connect to Vivaldi
        app = pywinauto.Application().connect(title_re=".*Vivaldi.*")
        window = app.window(title_re=".*Vivaldi.*")
        window.set_focus()
        print("Focused on existing Vivaldi window.")
    except pywinauto.findwindows.ElementNotFoundError:
        # If Vivaldi is not running, open a new window
        print("Vivaldi not found, opening a new window.")
        vivaldi_path = r'C:\Users\jylau\AppData\Local\Vivaldi\Application\vivaldi.exe'
        
        # Verify if the path is correct and the file is executable
        if os.path.exists(vivaldi_path):
            # Open Vivaldi with the provided URL
            subprocess.Popen([vivaldi_path, url])
            time.sleep(10)  # Wait for Vivaldi to open and load
        else:
            print(f"Vivaldi executable not found at {vivaldi_path}")


########################################################################
#Functions
def keystroke():
    print('Executing')
    auto.press('space')

def shutdown():
    print('Executing')
    os.system('shutdown -s')

def close_Tab():
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
        audio = rec.listen(source, timeout=10, phrase_time_limit=10.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        web.open_new(f'https://www.google.com/search?q={text}')

def go2Gpt():
        focus_vivaldi('https://chat.openai.com')
        start_talking()
##############################################################
#RunTime

secondary_Loop()


