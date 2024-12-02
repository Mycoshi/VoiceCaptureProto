import speech_recognition as sr
import os
import sys
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
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import subprocess
import threading
import pymongo


################################################################
#ISSUES AND NEEDS SECTION

#create dict of responses #NOT A DICT SQL DATABSE BECAUSE WE CAN UPDATE IT LIVE KEKW
#voice repsonse
#Translator implementation
#implent GPTREQUEST
#playsound is fucked needs local path
#need to be able to choose default web browser
#Enable choice of videos of youtube.
###### ISSUES ##########

#This is moved to Notes for speed

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
     print('Command Loop')
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
                elif "start talking" in text:
                    start_talking()
                elif "stop talking" in text:
                    stop_talking()
                elif "internet" in text:
                    focus_vivaldi()    
                elif '3030' in text:
                    os.system("taskkill /im vivaldi.exe /f")
                elif 'close tab' in text:
                    close_Tab()
                elif 'take notes' in text or 'open notes' in text:
                    take_Notes()
                elif 'open diary' in text:
                    open_Diary()
                elif 'add task' in text:
                     add_TasksWithVoice()
                     print('what task?')
                     time.sleep(5)
                     run_Tasks()
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
                    print('Restarting Command loop.')

        except sr.UnknownValueError:
            print('Returning to Command Loop UnknownValueError.')
        except sr.RequestError as e:
            print(f'Error with the speech recognition service: {e}')

            
#Talking Loops
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
   complete_note = ' '
   while Talking:
        try:
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=15.0)
                input_text = rec.recognize_google(audio).lower()
                
                if "i'm done" in input_text or 'quit' in input_text:
                    print("Stop talking.")
                    Talking = False
                    break

                auto.typewrite(f'{input_text}', interval=0.1)
                print('Is this correct?')
                with sr.Microphone() as source:
                    audio = rec.listen(source, phrase_time_limit=5.0)
                    confirm_text = rec.recognize_google(audio).lower()
                print(confirm_text)    
                if 'yes' in confirm_text:
                    auto.hotkey('ctrl', 'enter')
                else:
                    auto.hotkey('ctrl', 'a')
                    auto.press('delete')

        except Exception as e:
            print(f'Error during talking: {e}')
            time.sleep(1)

#Internet Functions
def focus_vivaldi(url=""):
    try:
        # Attempt to connect to an existing Vivaldi window
        app = Application().connect(title_re=".*Vivaldi.*")
        window = app.window(title_re=".*Vivaldi.*")
        window.set_focus()
        print("Focused on existing Vivaldi window.")
    except ElementNotFoundError:
        # If Vivaldi is not running, open a new window
        print("Vivaldi not found, opening a new window.")
        vivaldi_path = r'C:\Users\jylau\AppData\Local\Vivaldi\Application\vivaldi.exe'
        
        # Verify if the path is correct and the file is executable
        if os.path.exists(vivaldi_path):
            # Open Vivaldi with the provided URL
            if url:
                subprocess.Popen([vivaldi_path, url])
            else:
                subprocess.Popen([vivaldi_path])
            time.sleep(10)  # Wait for Vivaldi to open and load

            # Attempt to connect to the new Vivaldi window
            try:
                app = Application().connect(title_re=".*Vivaldi.*")
                window = app.window(title_re=".*Vivaldi.*")
                window.set_focus()
                print("Focused on new Vivaldi window.")
            except ElementNotFoundError:
                print("Failed to focus on new Vivaldi window.")
        else:
            print(f"Vivaldi executable not found at {vivaldi_path}")


########################################################################
#Functions
complete_note = ''
def chatterbox(keyphrase):
    global complete_note
    looping = True
    complete_note = ""  # Initialize complete_note if not already defined

    while looping:
        try:
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=10.0)
                text = rec.recognize_google(audio).lower()
                print(text)
                complete_note += text + " "
                print('text: ', text)
            
            # Check for the keyphrase to end the loop
            if f"end {keyphrase}" in text:
                complete_note = complete_note.replace(f"end {keyphrase}", "").strip()
                print(complete_note)
                looping = False  # Stop the loop
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio, restarting microphone...")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}. Restarting microphone...")
        except Exception as e:
            print(f"An error occurred: {e}. Restarting microphone...")

    return complete_note


def keystroke():
    print('Executing')
    auto.press('space')

def shutdown():
    print('Executing')
    os.system('shutdown -s')

def close_Tab():
    auto.hotkey('ctrl', 'w')
#Talk Functons
def add_TasksWithVoice():
    print('')
    note = ''
    try:
        with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=5.0)
                text = rec.recognize_google(audio).lower()
                print(text)
                note = text 
                print(text)
        if "end" in text:
                print(note)
    except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio, restarting microphone...")
    except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}. Restarting microphone...")
    except Exception as e:
                print(f"An error occurred: {e}. Restarting microphone...")
    return note
def run_Tasks():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    juno_tasks_path = os.path.join(script_dir, 'Tasks', 'JunoTasks.py')
    os.system(f'python "{juno_tasks_path}"')
def take_Notes():
    complete_note = ''
    looping = True
    while looping == True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = rec.listen(source, phrase_time_limit=10.0)
                text = rec.recognize_google(audio).lower()
                print(text)
                complete_note += text + " "
                if "stop listening" in text or 'end note':
                    complete_note = complete_note.replace("stop listening", "").strip()
                    looping = False
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio, restarting microphone...")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}. Restarting microphone...")
        except Exception as e:
            print(f"An error occurred: {e}. Restarting microphone...")

    current_timestamp = datetime.now()
    try:
        with open ('Notes.txt', 'a') as file:
            file.write(f'\n---{current_timestamp}---{complete_note}')
            print('Wrote to file')
    except:
        print('failure to write')

def open_Diary():
    print('diary open')
    chatterbox('diary')
    current_timestamp = datetime.now()
    try:
            
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["diaryDB"]

        mydict = { "Timestamp": f"{current_timestamp}", "Note": f"{complete_note}" }

        x = mycol.insert_one(mydict)

        print(f'Wrote to ID: {x.inserted_id}')
    except:
        print('Write Diary Failure')
        pass
    
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
       #TODO we need to webscrap our way to the selection with selenium, hotkeys and tab method proved cumbersome. SELIENUM IS NOT OK WITH VIVALDI

def go2google():
    print('Executing')
    with sr.Microphone() as source:
        audio = rec.listen(source, timeout=10, phrase_time_limit=10.0)
        text = rec.recognize_google(audio).lower().replace(' ','+' )
        web.open_new(f'https://www.google.com/search?q={text}')

def go2Gpt():
        focus_vivaldi('https://chat.openai.com')
##############################################################
#RunTime

secondary_Loop()

