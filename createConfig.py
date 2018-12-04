import configparser

config = configparser.ConfigParser()

#weather codes for different cities can be found on https://www.aviationweather.gov/metar
config['SETTINGS'] = {'City': 'Sofia',
                     'Offline': 'False',
                     'Adjust': 'False',
                     'weatherCode': 'LBSF'
                     }

with open('settings.ini', 'w') as configfile:
  config.write(configfile)