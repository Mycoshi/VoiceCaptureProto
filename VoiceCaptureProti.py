import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak')
    audio = r.listen(source)


    try:
        text = r.recognize_google(audio)
    except:
        print('failure error: Not recognized')


print(f'{text}')