import pyttsx3 as p
import randfacts
import speech_recognition as sr
#import pocketsphinx
import sel_web_driver as swd
from datetime import datetime

engine = p.init()  # initialize drivers for the text to speech module
recog = sr.Recognizer()  # retrieves audio from a microphone
assist = swd.voiceAssistantClass()

rate = engine.getProperty('rate')  # get rate of speech
engine.setProperty('rate',180)  # set rate of speech
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)  # 0 for male voice. 1 for female voice


def speak(text):
    engine.say(text)
    engine.runAndWait()  # waits till the speech is finished

def wish():
    hr = datetime.now().time()

date_time = datetime.now()
arr = assist.weather()
text = "Hi. I am your personal voice assistant megatron."
speak(text)
speak("Today is " + date_time.strftime("%d") + " of" + date_time.strftime("%b"))
speak("The temperature is " + arr[0] + " degree celsius and it is " + arr[1] + "in Trivandrum")
speak("How do you do sir")


def convert_speech_to_text(audio1):
    try:
        text1 = recog.recognize_google(audio1)
    except sr.UnknownValueError:
        text1 = " "
        print("Sorry, I didnt understand that.")
    except sr.RequestError as e:
        print("Error;{0}".format(e))
    return text1




with sr.Microphone() as source:
    recog.energy_threshold = 59.06161799517884
    recog.adjust_for_ambient_noise(source, 1.2)
    print("Listening...")
    audio = recog.listen(source)
    text = convert_speech_to_text(audio)  # sends audio to google api
    #text = recog.recognize_sphinx(audio)
    print(text)
    if "what" and "about" and "you" in text:
        speak("I am fine sir.")
speak("How can I help you today.")
print("How can I help you today.")

with sr.Microphone() as source:
    recog.energy_threshold = 59.06161799517884
    recog.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recog.listen(source)
    text2 = convert_speech_to_text(audio)
    print(text2)

if "wikipedia" and "information" in text2:
    print("what topics do you need information about")
    speak("what topics do you need information about")
    with sr.Microphone() as source:
        recog.energy_threshold = 59.06161799517884
        recog.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recog.listen(source)
        text2 = convert_speech_to_text(audio)
        print(text2)
        print("Certainly sir!Here is the information you requested")
        speak("Certainly sir!Here is the information you requested")
        assist.info(text2)
elif "play" and "video" in text2:
    print("what videos do you need me to search in youtube")
    speak("what videos do you need me to search in youtube")
    with sr.Microphone() as source:
        recog.energy_threshold = 59.06161799517884
        recog.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recog.listen(source)
        text2 = convert_speech_to_text(audio)
        print(text2)
        print("Certainly sir!Here is the video you requested")
        speak("Certainly sir!Here is the video you requested")
        assist.video(text2)
elif "news" in text2:
    print("Certainly sir!Here is the top headlines for the day in India")
    speak("Certainly sir!Here is the top headlines for the day in India")
    news = assist.news()
    for i in range(len(news)):
        print(news[i])
        speak(news[i])
elif "date" and "time" in text2:
    dAndT = datetime.now()
    print(dAndT)
    speak(dAndT)
elif "fact" in text2:
    print("Certainly sir!Here is the fact for the day")
    speak("Certainly sir!Here is the fact for the day")
    x = randfacts.get_fact()
    print(x)
    speak(x)
elif "joke" or "jokes" in text2:
    print("Certainly sir!Here is the joke you requested")
    speak("Certainly sir!Here is the joke you requested")
    arr = assist.jokes()
    print(arr[0])
    speak(arr[0])
    print(arr[1])
    speak(arr[1])
# elif "weather" and "today" in text2:
#     arr = assist.weather()
#     print("Certainly sir!Here is the current weather conditions in Trivandrum")
#     speak("Certainly sir!Here is the current weather conditions in Trivandrum")
#     print(arr)
#     speak(arr)







