import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {'City': 'Sofia',
                     'Offline': 'False',
                     'Adjust': 'False'}

with open('settings.ini', 'w') as configfile:
  config.write(configfile)