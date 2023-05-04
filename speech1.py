from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Initialize Chrome driver
driver = webdriver.Chrome(executable_path=r'D:\\Mental Challenge\\browser-assistant\\chromedriver.exe')
driver.maximize_window()

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id) 

# Define function to speak text
def speak(query):
    engine.say(query)
    engine.runAndWait()

# Define function to recognize speech using microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
        response = ""
        speak("Identifying speech..")
        try:
            response = recognizer.recognize_google(audio)
        except:
            response = "Error"
        return response.lower()

# Wait for Chrome to start up
time.sleep(3)
speak("Hello master! I am now online..")

# Open a new tab and navigate to Google
driver.execute_script("window.open('');")
window_list = driver.window_handles
driver.switch_to.window(window_list[-1])
driver.get('https://www.google.com/')

# Main loop
while True:   
    # Ask for user input
    speak("How can I help you?")
    voice = recognize_speech()
    print(voice)
    
    # Check for exit command
    if 'exit' in voice:
        speak('Goodbye Master!')
        driver.quit()
        break

    # Otherwise, perform a Google search
    else:
        query = voice + " images"
        if 'error' in query:
            speak("Sorry, I didn't understand.")
        else:
            search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            speak(f"Here are your {voice} images")
    
    time.sleep(5)
