from datetime import datetime
from sys import platform
import threading
import time

import pyttsx3
import wx
import pymetar
import feedparser

import pluginManager

if platform == "linux" or platform == "linux2":
    tts = pyttsx3.init() 
else:
    # this driver is windows specific, espeak for other non-max platforms 
    tts = pyttsx3.init('sapi5') 


tts.setProperty('rate', 150) #default rate is a bit too robotic, 150 makes it less so
weatherCode = "undeclared"

# this variable will be populated with a wx.FRAME object when this module is loaded from the main file
uinterface = None

commandList = ["repeat/say", "date/calendar", "time", "full time", "clear", "weather", "feed", "alarm", "help", "exit"]

def initialize(frame, code):
    global uinterface
    global weatherCode

    uinterface = frame
    weatherCode = code
    pluginManager.initialize(uinterface)

def getCommand(command):
    if command == "exit":
        exit()
    elif command.startswith("repeat") or command.startswith("say"):
        temp = command.split(' ', 1)
        if len(temp) > 1:
            say(temp[1])
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
        uinterface.console.Clear()
    elif command == "weather":
        getWeather()
    elif command == "feed":
        getRSS()
    elif command == "alarm":
        setAlarm()
    elif command == "help":
        printCommandList()
    else:
        pluginManager.executeCommand(command)

def say(text):
    tts.say(text)
    tts.runAndWait()

# need to make sure fetch is called only once for each city to avoid spamming requests, more commands can be found inside pymetar source code
def getWeather():
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

def printCommandList():
    uinterface.console.AppendText("Built-In Commands: \n")
    for k in commandList:
        uinterface.console.AppendText("\t"+k+"\n")
    uinterface.console.AppendText("\nCustom Commands: \n")
    for k in pluginManager.commandDispatch:
        uinterface.console.AppendText("\t"+k+"\n")
    uinterface.console.AppendText("\n")
