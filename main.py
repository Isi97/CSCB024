import configparser

import speech_recognition as sr
import wx

import commands

recognizer = sr.Recognizer()

config = configparser.ConfigParser()
config.read('settings.ini')

commandString = ""

#need to make MainWindow extend panel and add it to a frame, enables scrolling throguh UI elements with Tab
class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "CSCB024", size=(400, 600), style=wx.CAPTION )
        
        self.SetBackgroundColour('white')
        self.SetSizeHints(400,600,400,600)

        self.offlineMode = config.getboolean('SETTINGS', 'offline')
        self.adjustMode = config.getboolean('SETTINGS', 'adjust')

        self.buttonListen = wx.Button(self, label="Listen")
        self.buttonListen.Bind(wx.EVT_BUTTON, self.eventListen)

        self.buttonExit = wx.Button(self, label="Exit")
        self.buttonExit.Bind(wx.EVT_BUTTON, self.eventExit)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.offline = wx.CheckBox(self, label="Offline Mode: ")
        self.offline.SetValue(config.getboolean('SETTINGS', 'offline'))
        self.Bind(wx.EVT_CHECKBOX, self.eventOffline, self.offline)
        self.labelOffline = wx.StaticText(self, label="Using Google")
        
        self.rowOffline = wx.BoxSizer(wx.HORIZONTAL)
        self.rowOffline.Add(self.offline)
        self.rowOffline.Add(self.labelOffline)

        self.adjust = wx.CheckBox(self, label="Adjust for microphone noise: ")
        self.adjust.SetValue(config.getboolean('SETTINGS', 'adjust'))
        self.Bind(wx.EVT_CHECKBOX, self.eventAdjust, self.adjust)
        self.labelAdjust = wx.StaticText(self, label="Comprehension speed: normal")
        
        self.rowAdjust = wx.BoxSizer(wx.HORIZONTAL)
        self.rowAdjust.Add(self.adjust)
        self.rowAdjust.Add(self.labelAdjust)

        self.rowButton = wx.BoxSizer(wx.HORIZONTAL)
        self.rowButton.Add(self.buttonListen, wx.ALIGN_LEFT)
        self.rowButton.Add(self.buttonExit, wx.ALIGN_RIGHT)

        self.buttonAlarm = wx.Button(self, label="Set Alarm")
        self.buttonAlarm.Bind(wx.EVT_BUTTON, self.eventAlarm)
        self.rowAlarm = wx.BoxSizer(wx.HORIZONTAL)
        self.rowAlarm.Add(self.buttonAlarm)

        self.sizer.Add(self.rowButton)
        self.sizer.Add(self.rowOffline)
        self.sizer.Add(self.rowAdjust)
        self.sizer.Add(self.rowAlarm)

        self.console = wx.TextCtrl(self, size=(400,-1),style = wx.TE_MULTILINE | wx.TE_READONLY )
        self.sizer.Add(self.console, wx.EXPAND)
        

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        self.updateLabels()
        self.Centre()
        self.Show()

    def eventListen(self, event):
        commandString = self.getAudio()
        commands.getCommand(commandString)

    def eventOffline(self, event):
        temp = self.offline.GetValue()
        self.output("Offline mode set to: " + str(temp))
        self.offlineMode = temp
        if temp:
            self.labelOffline.Label = "Using Sphinx - accuracy reduced"
        else:
            self.labelOffline.Label = "Using Google"
        
    def eventAdjust(self, event):
        temp = self.adjust.GetValue()
        self.output("Adjust for ambient noise: " + str(temp))
        self.adjustMode = temp
        if temp:
            self.labelAdjust.Label = "Comprehension speed reduced"
        else:
            self.labelAdjust.Label = "Comprehension speed normal"

    def getAudio(self):
        with sr.Microphone(device_index=1) as source: #this index is currently making sure it's using a good mic, need to configure for other devices
            if self.adjustMode: 
                recognizer.adjust_for_ambient_noise(source)
            self.output("Listening for commands: ")
            audio = recognizer.listen(source)
        try:
            cmdS = ""
            if self.offlineMode:
                cmdS = recognizer.recognize_sphinx(audio)
                self.output("Sphinx heard: \t" + cmdS)
            else:
                cmdS = recognizer.recognize_google(audio)
                self.output("Google heard: \t" + cmdS)
            return cmdS
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    def eventExit(self, event):
        config.set('SETTINGS', 'offline', str(self.offlineMode))
        config.set('SETTINGS', 'adjust', str(self.adjustMode))
        with open('settings.ini', 'w+') as configfile:
            config.write(configfile)
        exit()

    def eventAlarm(self, event):
        pass

    def updateLabels(self):
        if self.adjustMode:
            self.labelAdjust.Label = "Comprehension speed reduced"
        else:
            self.labelAdjust.Label = "Comprehension speed normal"

        if self.offlineMode:
            self.labelOffline.Label = "Using Sphinx - accuracy reduced"
        else:
            self.labelOffline.Label = "Using Google"

    def output(self, text):
        self.console.AppendText(text+"\n")    
            
#print(sr.Microphone.list_microphone_names()) #use this to debug device indexes when running on new machine


app = wx.App()
frame = MainWindow()

'''
Assigning values to the commands module which are needed to interract with the GUI
This avoids passing around the 'bigger' config object, reading the file twice, and a circular import
'''
commands.uinterface = frame
commands.weatherCode = config['SETTINGS']['weathercode']

app.MainLoop()

