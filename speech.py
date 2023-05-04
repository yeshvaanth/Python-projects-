from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3


driver = webdriver.Chrome(executable_path=r'D:\\Mental Challenge\\browser-assistant\\chromedriver.exe')
driver.maximize_window()


engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voices',voices[1].id) 

engine.say('Hi I am a voice assistant')
engine.runAndWait()

recognizer=sr.Recognizer()
microphone=sr.Microphone()

def speak(query):
    engine.say(query)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        audio=recognizer.listen(source,phrase_time_limit=5)
        response=""
        speak("Identifying speech..")
        try:
            response=recognizer.recognize_google(audio)
        except:
            response="Error"
        return response

time.sleep(3)
speak("Hello master! I am now online..")

driver.execute_script("window.open('');")
window_list=driver.window_handles
driver.switch_to.window(window_list[-1])
driver.get('https://www.google.com/')

while True:   
    
    speak("How can I help you?")
    voice=recognize_speech().lower()
    print(voice)
    if 'exit' in voice:
        speak('Goodbye Master!')
        driver.quit()
        break

    else :
        while True:
            query=voice +" images"
            if query !='Error':
                break
        element=driver.find_element("name",'q')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
        if 'error' in voice:
            {}
        else:
            speak('Here is your '+voice+' images')

    time.sleep(5)
    
        
