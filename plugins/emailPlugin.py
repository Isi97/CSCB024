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

You can remove the check for fname != 'example' in the pluginManager module's loadPlugins function 
to see this plugin in action without having to create a new one
'''

import sys
import imaplib
import email
import datetime

IMAP_SERVER = "imap.gmail.com"
IMAP_USER = "golyamatoyaga"
IMAP_PASSWORD = "test1234&"

class Plugin:
    def __init__(self, outputfunction=None, dialogfunction=None):
        self.name = ["this calls action", "this will also call action"]

        if outputfunction is not None:
            self.out = outputfunction

        if dialogfunction is not None:
            self.showDialog = dialogfunction
        
        conn = imaplib.IMAP4_SSL(IMAP_SERVER)

        try:
            (retcode, capabilities) = conn.login(IMAP_USER, IMAP_PASSWORD)
        except:
            print (sys.exc_info()[1])
            sys.exit(1)


        conn.select(readonly=1)

        rv, data = conn.search(None, "ALL")
        if rv != 'OK':
            print("No messages found!")
            conn.close()
            return

        count = len(data[0].split())
        print('Number of messages: ', count)

        for i in range(count, 0, -1):
            typ, msg_data = conn.fetch(str(i), '(RFC822)')
            if typ != 'OK':
                print('ERROR getting message {0}'.format(num))
                conn.close()
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

        conn.close()

    def action(self):
        x = self.showDialog("User input required", "Enter a sentence: ")
        self.out("All the way from plugin land\t" + x)