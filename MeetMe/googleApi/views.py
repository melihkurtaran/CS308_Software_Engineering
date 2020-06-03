from django.shortcuts import redirect, render
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib import messages
from eventCalendar.models import Events
from django.urls import reverse

def gCalendar(request):
    flow = InstalledAppFlow.from_client_secrets_file(
    'googleApi/client_secrets.json',
    scopes=['https://www.googleapis.com/auth/calendar'])
    auth_uri = flow.authorization_url()

    credentials=flow.run_local_server()
    #print(credentials)                     ##
    service=build("calendar","v3",credentials=credentials)
    calendars=service.calendarList().list().execute()
    events=service.events().list(calendarId='primary').execute() ##get all events
    #print(events)  ##
    #print(type(events))
    #events=str(events)
    #messages.info(request,events) 
    # #summary  title
    userEvents = Events.objects.filter(userID=request.user)
    for calendarEvent in userEvents:
        #calendar = service.calendars().get(calendarId='primary').execute() ##get the main calendar
        event = {}
        event['summary']=calendarEvent.name
        event['start']={}
        start=str(calendarEvent.start).replace(' ','T')
        event['start']['dateTime']=start
        event['end']={}
        end=str(calendarEvent.end).replace(' ','T')
        event['end']['dateTime']=end

        event = service.events().insert(calendarId='primary', body=event).execute()


    userID = request.user.id  #id for auth user
    for item in events['items']:
        try:
            if item['status'] != 'cancelled':
                title=item['summary']
                start=item['start'].get('dateTime','NA')
                end=item['end'].get('dateTime','NA')
                if(start=='NA'):   ##For unspecified hour/minutes
                    start=item['start']['date']
                if(end=='NA'):
                    end=item['end']['date']
                #print(end.keys())
                print('{}, {}, {}'.format(title,start,end))
                event = Events(name=str(title), start=start, end=end, userID_id=userID)
                if not(Events.objects.filter(name=title,start=start,end=end, userID_id=userID).exists()): ##if it is not in db
                    event.save()
        except:
            print("exception occurred")


    return redirect('calendar')
