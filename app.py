from __future__ import print_function
import os
#from lib import locations
import openai
import json
import googlemaps
import math
from flask import Flask, redirect, render_template, request, url_for, jsonify
gmaps = googlemaps.Client("AIzaSyAUu5mSd5dc5VdMJ3lrcvCDXY-SzaGZMas")

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getUnavailable(unavailable):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Get today's date
        search_date = datetime.date.today()

        # Set the start and end time range for the specified day
        start_datetime = datetime.datetime.combine(search_date, datetime.time.min)
        end_datetime = datetime.datetime.combine(search_date, datetime.time.max)

        # Convert the datetime objects to ISO 8601 formatted strings
        time_min = start_datetime.isoformat() + 'Z'
        time_max = end_datetime.isoformat() + 'Z'

        # Call the Calendar API with the updated time range
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        # Call the Calendar API
        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # events_result = service.events().list(calendarId='primary', timeMin=now,
        #                                       maxResults=10, singleEvents=True,
        #                                       orderBy='startTime').execute()
        # events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))            
            end = event['end'].get('dateTime',event['end'].get('date'))
            name = event['summary']
            print("HERE-------------------------->")
            timezone = event['start'].get('timeZone')
            print(timezone)
            unavailable.append( (name,start,end) )

    except HttpError as error:
        print('An error occurred: %s' % error) 

# def calendar(events, unavailable):
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         service = build('calendar', 'v3', credentials=creds)
        
#         if not events:
#             print("No available schedule!")
#             return
#         for event in events:
#             if not (event[0],event[1],event[2]) in unavailable:
#                 addEvents = service.events().insert(
#                     calendarId='primary',
#                     body = {
#                         "summary": event[0]
#                         "start": {
#                             "date":
#                             "timeZone": America/Los_Angeles
#                             "dateTime"
#                         }
#                     }

#                 ).execute()
#         # Call the Calendar API


#     except HttpError as error:
#         print('An error occurred: %s' % error)





#from googlecalendarapi import getUnavailable 
# import googlemaps

# gmaps = googlemaps.Client("AIzaSyAUu5mSd5dc5VdMJ3lrcvCDXY-SzaGZMas")
'''
1 Hotel San Francisco, Mission Street, San Francisco, CA, USA ~ 2023-06-17T14:15:00-07:00 ~ 2023-06-17T14:45:00-07:00
UCB Hackathon ~ 2023-06-17T09:00:00-07:00 ~ 2023-06-18T18:30:00-07:00
testing 1 ~ 2023-06-18T05:00:00-07:00 ~ 2023-06-18T06:00:00-07:00
testing 2 ~ 2023-06-18T10:00:00-07:00 ~ 2023-06-18T11:00:00-07:00
'''

def parser(s):
    s.strip()
    i = s.find('[')
    s = s[i+2:-2].split('), (')
    res = []
    for x in s:
        x = x[1:-1]
        y = x.split("', '")
        res.append(y)
    return res

app = Flask(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=('GET', 'POST'))
def index():
    print("loading render")
    return render_template("index.html") # <- you have to render_template to see the webpage? why return aynthing else

@app.route('/generate', methods=('GET','POST'))
def index1():
    unavailable = []
    getUnavailable(unavailable)
    print(request.method)
    if request.method == "POST":
        events = request.json['tasks'] # THIS WILL BE A LIST OF LISTS WITH THE INFO OF TASKS
        for event in events:
            event[1] = get_coordinates(event[1])
            if not event[1]:
             
                event[1] = get_coordinates(events[0][1])

        # #     absCoord = abs(event[1][0]) + abs(event[1][1])
        
        # absCoord = []
        # for i in range(len(events)): 
        #     absCoord.append(abs(events[i][1][0]) + abs(events[i][1][1]))
      
        # print(absCoord)
        # if len(absCoord) > 1:
        #   distanceFromHome = []
        #   for i in range(len(absCoord[0:])):
        #     distanceFromHome.append(abs( absCoord[0] - absCoord[i]))
        # ascendingDistance= []
        # ascendingDistance = sorted(distanceFromHome)
        #for event in events
        #   for i in range(len(distancesFromHome))
        #   event[1] = distancesFromHome[i]
        
        # if len(absCoord) > 1:
        #[[name]. [lat,long], [priority]]
        
        
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(events, unavailable), # will be passed with google calendar events for AI to schedule
            temperature=0.6,
            max_tokens=1000
        )
       
        res=parser(response.choices[0].text)
        table = []
       
        for i in range(len(res)):
            temp = [ res[i][0], res[i][1][11:] + '-' + res[i][2][11:], res[i][3] ]
            table.append(temp)
           # table.append(res[i][1][11:] + '-' + res[i][2][11:])
        
        #print(table)
        return jsonify(f'{"res": ${table}}')
    return render_template('index.html')
        # response will return a new list with the most optimized order of tasks that work around events
        # print(response.choices[0].text) # used to test output
        # re = response.choices[0].text
        # print(response.choices[0].text)
        
        # this is whats printed from ^
        # "  [('UCB Hackathon', '2023-06-17T09:00:00-07:00', '2023-06-18T18:30:00-07:00'), ('testing 1', '2023-06-18T05:00:00-07:00', '2023-06-18T06:00:00-07:00'), ('gym', '60', '60', 'High'), ('grocery shopping', '30', '30', 'High'), ('hw', '60', '60', 'Medium'), ('testing 2', '2023-06-18T10:00:00-07:00', '2023-06-18T11:00:00-07:00')]"
        # print(type(re))
        # re = re.strip().replace("'", '"')
        # x = '{"res": ' + re + '}'
        # print(json.loads("{\"res\": " + re + "}"))
        # print(json.loads(x))
        # a = parser(re)
        # print(a)
        # print(type(a))
        # print(type(a[0]))
        # print("Parsed ~ ", a)
    

'''
@app.route('/convert', methods = ('GET','POST'))
def index2():
    return jsonify(result = get_coordinates(request.json['location']))
'''

def get_coordinates(address):
    if address:
        geocode_result = gmaps.geocode(address)
        if len(geocode_result) > 0:
            location = geocode_result[0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            return [lat, lng]
        else:
            return None
    else:
        return None
'''
todo qualities: [(name, duration, priority), (name, duration, priority), (name, duration, priority)]

-name
-duration
-priority
maybe
-fatigue
-locationle):
    

'''
def generate_prompt(todo, unavailable):

    #            todo: {todo}
    #            unavailable: {unavailable}
    #            schedule: """
    
#    return f"""Given a list of the times where I am unavailable with elements formatted as (event name, start time, end time) and the times formatted in yyyy-mm-dd combined with RFC3339 format of the time {unavailable}.  
#             Compose a list of tuples formatted as (event name, start time, end time) from a list of events, {todo}, which is formatted as (event name, distance from home, duration of task in minutes, priority ).  Make the highest priorty in the middle of the day.
#             Based on priority hierarchy, the following list of will go from highest priority to lowest, [Highest, high, medium, low, lowest]. If the priority is high or highest it may override any scheduling conflicts. Also take distance into account; Use the distance formula sqrt(longitude^2 + latitiude^2) to 
#             calculate the distance from current location to next closest tassk. The closer they are, the higher chance they should be next to each other in the schedule. Make sure these events don't overlap into unavaliable times. 
#             """ 
            
        # DONT REMOVE
    return f"""given a list of times I am unavailable with elements formatted as  (event name, start time , end time ) seperated by commas: {unavailable},
               create a schedule that will optimize every minute given a list of tasks with their respective duration in minutes and priority formatted as (task name, duration, location, priority), you can ignore the location index.
               for unavailable, make the third index 'Event' just like how the tasks have a priority setting in the third index ('High', 'Medium', 'Low')
               
               todo: [('hw', [1.000, 2.00], '60', 'Medium', ), ('gym', [3.000, 4.00], '60', 'High'), ('grocery shopping', [5.000, 6.000], '30', 'High')]
               unavailable: [('UCB Hackathon', '2023-06-17T09:00:00-07:00', '2023-06-18T18:30:00-07:00'), ('testing 1', '2023-06-18T05:00:00-07:00', '2023-06-18T06:00:00-07:00'), ('testing 2', '2023-06-18T10:00:00-07:00', '2023-06-18T11:00:00-07:00')]
               schedule: [('UCB Hackathon', '2023-06-17T09:00:00', '2023-06-18T18:30:00', 'Event'), ('testing 1', '2023-06-18T05:00:00', '2023-06-18T06:00:00', 'Event'), ('gym', '2023-06-18T06:00:00', '2023-06-18T07:00:00', 'High'), ('grocery shopping', '2023-06-18T07:00:00', '2023-06-18T07:30:00', 'High'), ('hw', '2023-06-18T07:30:00', '2023-06-18T08:30:00', 'Medium'), ('testing 2', '2023-06-18T10:00:00', '2023-06-18T11:00:00', 'Event')]"
               
               todo: {todo}
               unavailable: {unavailable}
               schedule: """ 


@app.route('/ethan', methods=('GET', 'POST'))
def ethan():
    return "ethan was here smiley face emoji"
 


if __name__ == "__main__":
    app.run()