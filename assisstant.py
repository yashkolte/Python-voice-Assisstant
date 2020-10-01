# ================================================ ASSISSTANT =============================================================
from __future__ import print_function
# MODULES REQUIRED..
# calender api

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# import datetime                                             # it is used for checking date and time
import os                                                   # it is here used for taking path
import time
import pytz
import random                                               #  for random integer
import smtplib                                              # for sending email
from selenium import webdriver                              # it is used for serching
# selenium for automated webpages
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyttsx3                                              # it is used for taking voices from computer
import speech_recognition as sr                             # it is used for audio recognition
# import pyaudio
import wikipedia                                            # it is used for directly getting answers by wikipedia
import selenium                                             # it is also used for testing sites and doing work in browsers opening link directly
import webbrowser
import subprocess                                           # it allow us to open sub process 
import requests
import json

# Some variables
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "febuary", "march", "april", "may", "june" ,"july" ,"august", "september", "october", "november", "december"]
DAY_EXTENSIONS = ["rd" , "th", "st", "nd"]
# start

# function to convert text to audio
def speak(audio):
    engine = pyttsx3.init('sapi5')                              # sapi5 is used to take voice of the windows
    voices = engine.getProperty('voices')
    # print(voices[0].id)                                       #there are two inbuild voices in the system male and female
    engine.setProperty('voice',voices[0].id)
    engine.say(audio)  
    engine.runAndWait()

# Take command form microphone and convert it to text
def takeCommand():
     # it takes microphone input from the user and returns string output
        
    r = sr.Recognizer() # it helps to detect audio from micro phone
    with sr.Microphone() as source:
        print("Listening. . .")
        r.pause_threshold = 1     # seconds of non speaking audio before a phase is considered
        audio = r.listen(source)
    try:
        print("Recongnizing. . .")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")

    except Exception as e:
        print(e)
        print("could not recognise. . .")
        return "None"
    return query

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
# Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

# Call the Calendar API
def get_events(day,service):
    date = datetime.datetime.combine(day,datetime.datetime.min.time())                     # min time on that day 
    end_date = datetime.datetime.combine(day,datetime.datetime.max.time())                 #max time on that date
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0].split(":")[0])

            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "AM"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time + "PM"
            speak(event['summary'] + 'at' + start_time)

# taking date from user
def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    
    if text.count("today")>0:
        return today
    
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        
        elif word in DAYS:
            day_of_week = DAYS.index(word)

        elif word.isdigit():
            day =  int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day ==-1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week  - current_day_of_week
        
        if dif < 0:
            dif += 7
            if text.count("next") >=1:
                dif +=7
        return today + datetime.timedelta(dif)
    if day != -1:
        return datetime.date(month = month, day = day , year = year)

# Function for greeting at starting..
def wishMe():
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 0 and hour<12:
        speak("Good morning")

    elif hour>=12 and hour <18:
        speak("Good Afternoon")
    
    else:
        speak("Good Evening")

    date =datetime.datetime.now().date()
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"I am Jarvis . Today's date is {date} and the time is {time} . please tell me how may i help you")

# function for sendind email.
def sendemail(reciever_email,content):
    sender_email= "sahuaman4444@gamil.com"
    reciever_email = "amanempirex4k@gmail.com"
    password = "Aman@x4k"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    print("Login Success")
    server.sendmail(sender_email,reciever_email,content)
    server.close()

def check_message():
    driver = webdriver.Chrome("D:\Softwares\chromedriver_win32\chromedriver.exe")
    driver.get('https://facebook.com/')
    username_space = driver.find_element_by_xpath('//*[@id="email"]')
    username_space.send_keys(7828737234)
    password_space = driver.find_element_by_xpath('//*[@id="pass"]')
    password_space.click()
    password_space.send_keys("amanempire")
    sign_in_button = driver.find_element_by_xpath('//*[@id="u_0_b"]')
    sign_in_button.click()

    time.sleep(6)

    message = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div/div[1]/div[2]/div[4]/div[1]/div[2]/span/div/div[1]')
    message.click()

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name, "w") as  f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

def temperature():
    api_key = "36dd267ebc8442164b40cabe86763f6f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = query
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        speak(" Temperature" +
                        str(current_temperature-273).split(".")[0] + " degree celcius" +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidiy) +
            "\n wheather = " +
                        str(weather_description)) 
    
    else: 
        print(" City Not Found ")

def news():
    url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=753fa441ed08439bb18b4ecdab5d69c2"
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict["articles"]
    count = 1
    index = 0
    news_num = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]

    while count<11:
        speak(f"{news_num[index]} news is {arts[count]['title']}")
        print(f"{news_num[index]} news is {arts[count]['title']}")
        print("For more :",arts[count]["url"],"\n")
        count+=1
        index+=1
        
def match():
    match_data = requests.get("https://cricapi.com/api/cricketScore?unique_id=1225248&apikey=D4WYYjhOZJWaNU27GvBoUY87SbZ2").text
    json_data = json.loads(match_data)
    current_score = json_data["stat"]
    team1 = json_data["team-1"]
    team2 = json_data["team-2"]
    speak(f"score is {current_score}")
    speak(team1)
    speak(team2)

# main execution begins from here
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if "hello" in query:
            speak("hello sir")
            speak("what can i do for you")
            query = takeCommand().lower()

            if "your name" in query or "about you" in query:
                speak("my name is jarvis . i m your persoanl voice assissant. i will help you serching things and also do some other stuff for your easyness")

            elif "how are you" in query or "what'sup" in query:
                speak("i am fine. what about you")
                query = takeCommand().lower()
                if "i am fine" in query or "i am good" in query or "i am perfect" in query:
                    speak("it's good to hear that")
                elif "sad" in query or "dissappointed" in query or "not ok" in query or "not good" in query:
                    speak("Don't worry sir, everything will alright. i am there for you")
                    query = takeCommand().lower()
                    if "thank you" in query or "thankyou" in query:
                        speak("its my pleasure sir. take care")
                    elif "ok" in query:
                        speak("yes sir see you again")
                    else:
                        pass
                else:
                    pass

            elif "the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir the time is {strTime} ")
            
            elif "the date" in query:
                date =datetime.datetime.now().date()
                speak(f"sir todays date is {date} ")
            
            elif "about me" in query or "who i am" in query:
                speak("sir your name is Aman sahu . your age is 19 . and your are studying in Atria institute of technology.")
                speak(" your mobile number is 7828737234 . and also your email is amanempirex4k@gmail.com")
                speak("you are living in bhopal . your home address is shed 2 patel nagar mandideep")
            
            # For searching something
            elif "wikipedia" in query:
                os.system("cls")
                speak("searching wikipedia. . .")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences = 2)
                speak("according to wikipedia")
                print(results)
                speak(results)

            elif "search" in query:
                query = query.replace("search","")
                url = 'https://google.com/search?q='+ query
                webbrowser.get().open(url)
                speak("here is what i found for")

            elif "find location" in query:
                speak("name of location you want me to find")
                location = takeCommand()
                url = 'https://google.nl/maps/search/' + location + '/&amp;'
                webbrowser.get().open(url)
                speak("here is the location" + location)
            
            elif "temperature" in query:
                query = query.replace("temperature in","")
                temperature()

            # For opening sites
            elif "open youtube" in query:
                speak("opening youtube")
                webbrowser.open("https://youtube.com")
            
            elif "open google" in query:
                speak("opening google")
                webbrowser.open("https://google.com")

            elif "open facebook" in query:
                speak("opening Facebook")
                webbrowser.open("https://facebook.com")
            
            elif "open stack overflow" in query:
                speak("opening stack overflow")
                webbrowser.open("https://stackoverflow.com")

            # for doing some actions
            elif "facebook message" in query or "facebook messages" in query:
                check_message()
                speak("it looks like you have some")

            elif "make a note" in query or "write this" in query or "remember this" in query:
                speak("what would you like me to write down ? ")
                text = takeCommand().lower()
                note(text)
                speak("I have made a note.")

            elif "play music" in query:
                speak("playing music")
                music_dir = 'D:\\Music'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[random.randint(0,len(songs)-1)]))

            elif "open visual studio" in query:
                speak("opening visual studio")
                path = "C:\\Users\\Aman\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)

            elif "open whatsapp" in query:
                speak("opening whatsapp")
                path = "C:\\Users\\Aman\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                os.startfile(path)
            
            elif "news" in query:
                speak("Top ten news headlines are")
                news()

            elif "live score" in query or "score" in query or "cricket" in query:
                speak("the live score is")
                match()

            elif "send email" in query:
                try:
                    speak("whats should i say")
                    content = takeCommand()
                    reciever_email = "amanempirex4k@gmail.com"
                    sendemail(reciever_email,content)
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("sorry sir i'm unable to process the email")

            elif "events" in query or "event" in query:
                speak("Tell me the day or day of the event")
                SERVICE = authenticate_google()
                print("Start")
                text = takeCommand()

                CALENDER_STR = ["do i have ", "what do i have", "am i busy","what i have on", "on that day"]
                for phrase in CALENDER_STR:
                    if phrase in text.lower():
                        date = get_date(text)
                        if date:
                            get_events(date,SERVICE)
                        else:
                            speak("please try again")
            
            else:
                speak("could not recognize. say again")
                query = takeCommand().lower()
        # for extra commands
        elif "ok" in query:
            speak("yes sir")                    

        elif "good bye" in query or "bye" in query or "quit" in query or "exit" in query or "sleep" in query:
            speak("bye sir")
            os.system("cls")
            exit()


        elif "good night" in query:
            speak("bye sir. good night")
            os.system("cls")
            exit()
            
        elif "thank you" in query:
            speak("its my pleasure sir.")

        else:
            pass