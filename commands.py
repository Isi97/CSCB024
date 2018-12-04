from datetime import datetime
import threading
import time

import pyttsx3
import wx
import pymetar
import feedparser


tts = pyttsx3.init('sapi5') #this driver is windows specific, espeak for other non-max platforms 
#but windows pip currently not installing drivers need to be downloaded manually to test

tts.setProperty('rate', 150)
weatherCode = ""

#this variable will be populated with a wx.FRAME object when this module is loaded from the main file
uinterface = None

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
        return 1
    elif command == "weather":
        getWeather()
    elif command == "feed":
        getRSS()
    elif command == "alarm":
        setAlarm()
    
def say(text):
    tts.say(text)
    tts.runAndWait()

#need to make sure fetch is called only once for each city to avoid spamming requests
def getWeather():
    print(weatherCode)
    fetch = pymetar.ReportFetcher(weatherCode)
    pars = pymetar.ReportParser(fetch.FetchReport())
    pars.ParseReport()
    uinterface.console.AppendText(str(pars.Report.temp) + " C " + str(pars.Report.weather) + "\n")

def getRSS():
    link = ""
    dialog = wx.TextEntryDialog(uinterface, "Enter RSS Feed link", "User input required")
    if dialog.ShowModal() == wx.ID_OK:
        NewsFeed = feedparser.parse(dialog.GetValue())
        uinterface.console.AppendText("\nStarting RSS feed: \n\n")
        for entry in NewsFeed.entries:
            uinterface.console.AppendText(entry.title + "\n\n")
        uinterface.console.AppendText("\nEnd of RSS feed\n")

def setAlarm():
    dialog = wx.TextEntryDialog(uinterface, "Enter minutes until alarm rings", "User input required")
    if dialog.ShowModal() == wx.ID_OK:
        seconds = int(dialog.GetValue()) * 60
        alarmThread = threading.Thread(target=lambda: alarm(seconds))
        alarmThread.start()

def alarm(seconds):
    time.sleep(seconds)
    uinterface.console.AppendText("\n\n###Alarm Completed###\n\n")

#voices = tts.getProperty('voices')
#tts.setProperty('voice', voices[1].id)
