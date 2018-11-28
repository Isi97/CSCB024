import speech_recognition as sr
import wx
import commands
import configparser

recognizer = sr.Recognizer()

config = configparser.ConfigParser()
config.read('settings.ini')

commandString = ""

#need to make this extend panel and not frame
class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "CSCB024", size=(600, 300), style=wx.CAPTION )
        #panel = wx.Panel(self, wx.ID_ANY)
        self.SetBackgroundColour('white')
        self.SetSizeHints(600,300,600,300)

        self.offlineMode = config.getboolean('DEFAULT', 'offline')
        self.adjustMode = config.getboolean('DEFAULT', 'adjust')

        self.buttonListen = wx.Button(self, label="Listen")
        self.buttonListen.Bind(wx.EVT_BUTTON, self.eventListen)

        self.buttonExit = wx.Button(self, label="Exit")
        self.buttonExit.Bind(wx.EVT_BUTTON, self.eventExit)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.offline = wx.CheckBox(self, label="Offline Mode: ")
        self.offline.SetValue(config.getboolean('DEFAULT', 'offline'))
        self.Bind(wx.EVT_CHECKBOX, self.eventOffline, self.offline)
        self.labelOffline = wx.StaticText(self, label="Using Google")
        
        self.rowOffline = wx.BoxSizer(wx.HORIZONTAL)
        self.rowOffline.Add(self.offline)
        self.rowOffline.Add(self.labelOffline)

        self.adjust = wx.CheckBox(self, label="Adjust for microphone noise: ")
        self.adjust.SetValue(config.getboolean('DEFAULT', 'adjust'))
        self.Bind(wx.EVT_CHECKBOX, self.eventAdjust, self.adjust)
        self.labelAdjust = wx.StaticText(self, label="Comprehension speed normal")
        
        self.rowAdjust = wx.BoxSizer(wx.HORIZONTAL)
        self.rowAdjust.Add(self.adjust)
        self.rowAdjust.Add(self.labelAdjust)

        self.buttonRow = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonRow.Add(self.buttonListen, wx.ALIGN_LEFT)
        self.buttonRow.Add(self.buttonExit, wx.ALIGN_RIGHT)


        self.sizer.Add(self.buttonRow)
        self.sizer.Add(self.rowOffline)
        self.sizer.Add(self.rowAdjust)

        self.console = wx.TextCtrl(self, size=(300,-1),style = wx.TE_MULTILINE | wx.TE_READONLY )
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
        config.set('DEFAULT', 'offline', str(self.offlineMode))
        config.set('DEFAULT', 'adjust', str(self.adjustMode))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        exit()

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
app.MainLoop()

