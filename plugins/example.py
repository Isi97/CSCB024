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

class Plugin:
    def __init__(self, outputfunction=None, dialogfunction=None):
        self.name = ["this calls action", "this will also call action"]

        if outputfunction is not None:
            self.out = outputfunction

        if dialogfunction is not None:
            self.showDialog = dialogfunction

    def action(self):
        x = self.showDialog("User input required", "Enter a sentence: ")
        self.out("All the way from plugin land\t" + x)