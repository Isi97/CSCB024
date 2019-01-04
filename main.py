import ConfigParser

import speech_recognition as sr
import wx

import commands

recognizer = sr.Recognizer()

config = ConfigParser.ConfigParser()
config.read('settings.ini')

commandString = ""

# need to make MainWindow extend panel and add it to a frame, enables scrolling throguh UI elements with Tab
class MainWindow(wx.Frame):
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 600

        wx.Frame.__init__(self, None, wx.ID_ANY, "CSCB024", size=(self.WIDTH, self.HEIGHT), style=wx.CAPTION )
        self.SetBackgroundColour('white')
        self.SetSizeHints(self.WIDTH,self.HEIGHT,self.WIDTH,self.HEIGHT)

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

        self.textCommands = wx.TextCtrl(self, size=(self.WIDTH, -1), style = wx.TE_PROCESS_ENTER)
        self.textCommands.SetHint("Command + Enter")
        self.textCommands.Bind(wx.EVT_TEXT_ENTER, self.eventSubmit)
        self.rowCommands = wx.BoxSizer(wx.HORIZONTAL)
        self.rowCommands.Add(self.textCommands)


        self.commandCombo = wx.ComboBox(self)
        self.commandComboRun = wx.Button(self, label="run")
        self.commandComboRun.Bind(wx.EVT_BUTTON, lambda x: commands.getCommand(self.commandCombo.GetValue()))
        self.rowCommandsUI = wx.BoxSizer(wx.HORIZONTAL)
        self.rowCommandsUI.Add(self.commandCombo)
        self.rowCommandsUI.Add(self.commandComboRun)

        self.sizer.Add(self.rowButton)
        self.sizer.Add(self.rowOffline)
        self.sizer.Add(self.rowAdjust)
        self.sizer.Add(self.rowCommandsUI)

        self.console = wx.TextCtrl(self, size=(self.WIDTH,-1),style = wx.TE_MULTILINE | wx.TE_READONLY )
        self.sizer.Add(self.console, wx.EXPAND)

        self.sizer.Add(self.rowCommands)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

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
        with sr.Microphone(device_index=2) as source: # index = can be added as a parameter for Microphone in the event of multiple connected audio inputs
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
    
    def eventSubmit(self, event):
        command = self.textCommands.GetValue()
        self.textCommands.Clear()
        self.console.AppendText(command+"\n")
        commands.getCommand(command)

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

    def loadCommands(self):
        self.commandCombo.SetItems(commands.getCommandList())
    def getLine(self):
        line_number = len( self.console.GetRange( 0, self.console.GetInsertionPoint() ).split("\n") )
        return self.console.GetLineText(line_number-2)
            
#print(sr.Microphone.list_microphone_names()) #use this to debug device indexes when running on new machine
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#   print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))



def initialize():
    app = wx.App()
    frame = MainWindow()

    # Assigning values to the commands module which are needclsed to interract with the GUI
    wc = config.get("SETTINGS","weathercode")
    commands.initialize(frame=frame, code=wc)

    frame.loadCommands()
    frame.output("Finished loading.")
    frame.output("Type 'help' for a list of commands.")

    app.MainLoop()



if __name__ == "__main__":
    initialize()
