'''
This class is used to add functionality to the base program
All files with this structure in the /plugins folder will be automatically loaded into the program on startup
The file must contain a class called 'Plugin'. The content of list 'name' will be used to call the added function during runtime
A function 'action' must be present, this is the code which will be executed when using the plugin

Two functions will be passed onto the plugin by the main program:
    outputfunction can be used to output text to the programs interface
    dialogfunction can be used to retrieve information from the user with the following syntax:
        showDialog(title, message) returns either a string entered by the user or -1 if they cancled the command

Having multiple plugins use the same name variable will result in the one loaded last being the one using the command

Display number of message, number of unread message and execute commands e.g read last email...
'''

import sys
import imaplib
import email
import datetime
import time
import threading
import wx

#hardcoded IMAP server & credentials
IMAP_SERVER = "imap.gmail.com"
IMAP_USER = "golyamatoyaga"
IMAP_PASSWORD = "test1234&"
#threshold in minutes to concern message as 'NEW', Probably can become dependent on bandwidth  & number of messages 
THRESHOLD = 1

class Plugin:
    conn = None
    stopThread = False
    def __init__(self, outputfunction=None, dialogfunction=None):
        self.name = ["this calls action", "this will also call action"]

        if outputfunction is not None:
            self.out = outputfunction

        if dialogfunction is not None:
            self.showDialog = dialogfunction
        
        self.conn = imaplib.IMAP4_SSL(IMAP_SERVER)

        t = threading.Thread(target=self.worker)
        t.start()

        frame2 = SecondFrame(parent=None, id=-1)
        frame2.Show()

        try:
            (retcode, capabilities) = self.conn.login(IMAP_USER, IMAP_PASSWORD)
        except:
            print (sys.exc_info()[1])
            self.stopThread = True


        for i in range(self.getNumberOfMessages(), 0, -1):
            typ, msg_data = self.conn.fetch(str(i), '(RFC822)')
            if typ != 'OK':
                print('ERROR getting message {0}'.format(num))
                self.conn.close()
                return
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode("utf-8"))
                    #for header in [ 'subject' ]:
                        #print( msg[header])
                    #print(msg['Date'])
                    date_tuple = email.utils.parsedate_tz(msg['Date'])
                    if date_tuple:
                        local_date = datetime.datetime.fromtimestamp(
                            email.utils.mktime_tz(date_tuple))
                        print( 'Date: ' ,local_date, 'Subject: ' , msg['subject'])
                        #print ("Local Date:", \
                            #local_date.strftime("%a, %d %b %Y %H:%M:%S"))

        self.conn.close()

        #while True:
            #time.sleep(2)
            #print('Main thread')
        

    def action(self):
        x = self.showDialog("User input required", "Enter a sentence: ")
        self.out("All the way from plugin land\t" + x)
    
    def getNumberOfMessages(self):
        """tries to count all messages"""
        if self.conn == None:
            return 0

        self.conn.select(readonly=1)

        rv, data = self.conn.search(None, "ALL")
        if rv != 'OK':
            print("No messages found!")
            self.conn.close()
            return 0

        count = len(data[0].split())
        #print('Number of messages: ', count)

        return count

    def worker(self):
        """thread worker function"""
        self.stopThread = False
        while True:
            if self.stopThread == True:
                print('notification thread stopped')
                return
            time.sleep(2)
            if self.conn != None:
                print(self.conn)
                #wx.CallAfter(self.gauge.SetValue, x)
            print ('Worker')
        return

class SecondFrame(wx.Frame):
    box = None
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Popup Frame',
                            size=(350, 200))
        panelSecond = wx.Panel(self)

        self.box = wx.BoxSizer(wx.VERTICAL) 
        lbl = wx.StaticText(panelSecond,-1,style = wx.ALIGN_CENTER) 
        txt = "Python GUI development"  
        font = wx.Font(10, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        lbl.SetFont(font) 
        lbl.SetLabel(txt) 
            
        self.box.Add(lbl,0,wx.ALIGN_CENTER) 

        lbl = wx.StaticText(panelSecond,-1,style = wx.ALIGN_CENTER) 
        txt = "another"  
        lbl.SetFont(font) 
        lbl.SetLabel(txt) 
        lbl.Wrap(200)

        self.box.Add(lbl,0,wx.ALIGN_CENTER) 

        panelSecond.SetSizer(self.box) 
        self.Centre() 

        print(len(self.box.GetChildren()))

        #buttonCloseFrame = wx.Button(panelSecond, label="OK!",size=(50, 50))

        #box.Add(buttonCloseFrame,0,wx.ALIGN_CENTER)

        #self.Bind(wx.EVT_BUTTON, self.ClosePress,  buttonCloseFrame)
        self.Bind(wx.EVT_BUTTON, self.ClosePress)
 
    def ClosePress(self, event):
        self.Destroy()