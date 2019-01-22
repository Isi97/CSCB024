import os
import sys
import wx

pluginPath = "plugins/"
commandDispatch = {}

# this will be passed on from the commands module and used to generate UI or affect the output console
uinterface = None

def executeCommand(commandname):
    if commandname in commandDispatch:  
        commandDispatch.get(commandname)()

def initialize(frame):
    global uinterface
    uinterface = frame
    loadPlugins()
 
# This can be used by plugins to request data from the user and check against -1 to continue
# will be passed by reference to plugins together with the output function
def showDialog(title, message):
    dialog = wx.TextEntryDialog(uinterface, message, title)
    if dialog.ShowModal() == wx.ID_OK:
        return dialog.GetValue()
    else:
        return -1

def output(content):
        uinterface.console.AppendText(content + "\n")


def loadPlugins():
        plugins = {}
        sys.path.insert(0, pluginPath)
        for f in os.listdir(pluginPath):
                fname, ext = os.path.splitext(f)
                if ext == '.py' and fname != 'example':
                        module = __import__(fname)
                        if hasattr(module, 'Plugin') :
                                plugins[fname] = module.Plugin(output, showDialog)
        sys.path.pop(0)

        for p in plugins.values():
                for name in p.name:
                        commandDispatch[name] = p.action
