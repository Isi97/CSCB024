# CSCB024

## Running on ubuntu 18.04 prerequisites

```
sudo apt install python3-pip
```

dependencies required by wxpython:

```
sudo apt-get install libgtk-3-dev libpulse-dev
```

```
sudo apt-get install libwebkitgtk-3.0-dev
```

pyaudio:

```
sudo apt-get install python3-pyaudio
```

```
sudo apt-get install espeak
```

## Installing project dependencies

next one may take time...
```
pip3 install wxpython
```

other
```
pip3 install SpeechRecognition pyttsx3 pymetar feedparser
```


## dependencies
wxpython

speechrecognition

pyaudio

pocketsphinx

pyttsx3

pypiwin32

pymetar

feedparser

praw (for plugins/socialPlugin reddit API wrapper)

## Python 3.5

make sure settings.ini and a plugins folder are present in the directory

different weather codes for the configuration file can be found at https://www.aviationweather.gov/metar

an example with instructions on how to create plugins can be found in /plugins, example.py is not recognized as a plugin by the program

current email address being used for testing purposes: golyamatoyaga@gmail.com