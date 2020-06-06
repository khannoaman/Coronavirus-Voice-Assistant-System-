import requests
from bs4 import BeautifulSoup
import pandas as pd
from threading import *
import pyttsx3
import speech_recognition as sr
import datetime
import re
import numpy as np


class Country(Thread):

    countriesData=None
    countriesName=None

    def run(self):
        try:
            url = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdUOA?Si9"

            r = requests.get(url)
            htmlcontent = r.content

            soup = BeautifulSoup(htmlcontent, "lxml")
            table = soup.find("table")
            tr = table.find_all("tr")
            data = []
            for i in tr:
                def process(i):
                    i = i.text
                    i = i.strip()
                    i = re.sub(r'\+', "", i)
                    i = re.sub(r',', "", i)
                    return i

                row = [j for j in map(process, i.find_all(["th", "td"]))]
                data.append(row)

            df = pd.DataFrame(data)
            df.columns = df.iloc[0, :]
            df = df.iloc[:, [1, 2, 4, 6, 8]]
            df = df.drop(0)
            df = df.replace("", np.nan)
            df = df.dropna(subset=["CountryOther"])
            df.columns = ["Location", "Confirmed", "Deceased", "Recovered", "Active"]
            df.iloc[6, 0] = "world"
            df.set_index("Location", drop=True, inplace=True)
            df = df.drop("Total:")
            df.fillna(0, inplace=True)
            df = df.reindex(columns=["Confirmed", "Active", "Recovered", "Deceased"])
            df.to_csv("CountryData.csv")
            Country.countriesData = df
            Country.countriesName = list(df.index)



        except:
            df=pd.read_csv("CountryData.csv",index_col="Location")
            Country.countriesData = df
            Country.countriesName = list(df.index)







class States(Thread):

    statesData=None
    statesName=None
    def run(self):
        try:
            url = "https://www.mygov.in/covid-19"

            r = requests.get(url)
            htmlcontent = r.content

            soup = BeautifulSoup(htmlcontent, "lxml")

            df = pd.read_html(soup.prettify())[0]
            df.columns = ["Location", "Confirmed", "Active" , "Recovered","Deceased"]
            df = df.set_index("Location", drop=True)
            df.to_csv("StateData.csv")
            States.statesData = df
            States.statesName = list(df.index)


        except:
            df=pd.read_csv("StateData.csv",index_col="Location")
            States.statesData = df
            States.statesName = list(df.index)




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold=500
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said: {}".format(query))

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def find_place(query,s,c):
   a=[]
   for i in s.statesName:
       if i in query:
           a.append(i)

   for i in c.countriesName:
       if i in query:
           a.append(i)


   return a



def Exit(query):
    for i in ["close","exit","bye"]:
        if i in query:
            return 1
