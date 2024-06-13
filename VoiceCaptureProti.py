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
#create dict of responses #NOT A DICT SQL DATABSE BECAUSE WE CAN UPDATE IT LIVE KEKW
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
sound_path = os.path.join(script_dir, 'assets', 'Sounds', 'processing.mp3')
################################################################
#Calibration
with sr.Microphone() as source:   
     print("Please wait. Calibrating microphone...")   
     # listen for 5 seconds and calculate the ambient noise energy level   
     rec.adjust_for_ambient_noise(source, duration=5)
     rec.dynamic_energy_threshold = True  
     
################################
#todo Scared of why this works, it runs once then turns false?
#Core Functions
def listen_with_pause_detection(recognizer, source, pause_limit=2.0, phrase_time_limit=10):
    """
    Listen to audio and recognize speech. Stop if a long pause is detected.
    :param recognizer: An instance of sr.Recognizer()
    :param source: An audio source
    :param pause_limit: Maximum allowed pause duration (in seconds) before stopping
    :param phrase_time_limit: Maximum duration for a single phrase (in seconds)
    :return: Recognized text
    """
    print("Listening for speech...")
    start_time = time.time()
    while True:
        try:
            audio = recognizer.listen(source, timeout=pause_limit, phrase_time_limit=phrase_time_limit)
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")

            # Reset the timer on successful recognition
            start_time = time.time()
            return text  # For continuous recognition, you might want to append to a list instead

        except sr.WaitTimeoutError:
            # Check if the pause exceeds the allowed pause limit
            if time.time() - start_time > pause_limit:
                print("Long pause detected, stopping...")
                break
            else:
                print("Pause detected, waiting for more speech...")
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            break

    return None

def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        recognized_text = listen_with_pause_detection(recognizer, source)
        if recognized_text:
            print(f"Final recognized text: {recognized_text}")
        else:
            print("No valid speech was recognized or long pause detected.")

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
                    print('not listening')
                    text = rec.recognize_google(audio).lower()
                    print(text)
                    if 'listen' in text:
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
    with sr.Microphone() as source:
        audio = rec.listen(source, timeout=5 ,phrase_time_limit=60.0)
        text = rec.recognize_google(audio).lower()
        print(f'{text}, written in notes')
        try:
            with open ('example.txt', 'a') as file:
                file.write(f'\n---{text}')
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
        ################################
        #TODO WEBSCRAP LINKS ON YOUTUBE
        #RETIRING TAB LOCATOR CAUSE I HATE IT GO BACK TO WEBSCRAPER
        #if 'first one' in text:
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('tab')
        #    auto.press('enter')
        #    time.sleep(1)
        #    auto.press('enter')
        #    time.sleep(1)
        #    auto.press('left')
        #else : 
        #    secondary_Loop()

       

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
        playsound(r'C:\Users\jylau\Documents\github\VoiceCaptureProti\assets\Sounds\input.mp3')
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=2.0)
            text = rec.recognize_google(audio).lower()


            #selenium dcriver is a fucking pain compared to webrowser BUT ILL FIGURE IT THE FUCK OUTblank
            driver = webdriver.Firefox()
            driver.get("https://www.python.org")


##############################################################
#RunTime

Core_Loop()


