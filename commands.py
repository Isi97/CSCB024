import pyttsx3
from datetime import datetime
import main


tts = pyttsx3.init('sapi5') #this driver is windows specific, espeak for other non-max platforms 
#but windows pip currently not installing drivers need to be downloaded manually to test

tts.setProperty('rate', 150)


def getCommand(command):
    if command == "exit":
        exit()
    elif command.startswith("repeat"):
        #temp = command.split(' ', 1)
        say(command)
    elif command == "date" or command == "calendar":
        date = datetime.now()
        say(date.strftime('%d') + "th of " + date.strftime('%B'))
    elif command == "time":
        date = datetime.now()
        say(date.strftime('%I %M %p'))
    elif command == "full time":
        date = datetime.now()
        say(date.strftime('%X'))
    elif command == "clear":
        main.frame.console.Clear()
    

def say(text):
    tts.say(text)
    tts.runAndWait()


from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def getWeather(city):
    try:
        with closing(get("https://openweathermap.org/find?q="+city, stream=True)) as resp:
            data = resp.content

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
    
    html = BeautifulSoup(data, 'html.parser')
    row = html.find_all('div')
    for r in row:
        print(r.text + "\n")


#getWeather("Sofia")


#voices = tts.getProperty('voices')
#tts.setProperty('voice', voices[1].id)