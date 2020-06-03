from django.shortcuts import render
from django.contrib.auth.models import User
from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents
import calendar
from datetime import datetime, timedelta
import pytz
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from dateutil.relativedelta import relativedelta
import json
# Create your views here.
# Create your views here.
def myMeetings(request):
    user = request.user
    partMeetings =[]
    #all_events = Events.objects.all()

    #get all the meetings that the current user is the creator
    userMeetings = Meetings.objects.filter(creatorID = user)

    #get all the participated meetings (all the meetings that we have been invited)
    #first find the ids of the meetings that ve have been invited to
    meetingIDs = MeetingParticipation.objects.filter(partID = user.id)

    #search these meeting ids in meetings
    for i in meetingIDs:
        meeting = Meetings.objects.filter(meetingID = i.meetingID.meetingID)
        for k in meeting:
            if k.creatorID != user:
                try:
                    tz = pytz.timezone('Europe/Istanbul')
                    k.start = k.start.astimezone(tz)
                    k.end = k.end.astimezone(tz)
                    creatorUsername = User.objects.filter(id = k.creatorID.id)
                    partMeetings.append([k, creatorUsername[0].username])
                except AttributeError:
                    creatorUsername = User.objects.filter(id = k.creatorID.id)
                    partMeetings.append([k, creatorUsername[0].username])
    
    #convert time for the creator's meetings
    for i in userMeetings:
        try:
            #this is the timezone to be converted
            tz = pytz.timezone('Europe/Istanbul')
            #convert event.start to tz timezone, event.start was utc before!!!
            i.start = i.start.astimezone(tz)
            i.end = i.end.astimezone(tz)
        except AttributeError:
            continue
    
    context = {
        'createdMeetings': userMeetings,
        'partMeetings': partMeetings,
    }
    return render(request,'mymeetings/myMeetings.html',context)  ##testing
    #return render(request,'eventCalendar/addMeeting.html',context)



def voting(request):
    user=request.user
    #meetingID=16     ###default

    #print(request)
    
    if(request.POST.get('ids')!=None):
        print("True")
        print(request.POST.get('ids'))
    else:
        print(request.POST.get('ids'))
        print("False")
        #print(request.POST['ids'] )   ##
        #MeetingEventIDs=request.POST['ids']   ## 
    if request.method == 'POST':
        print(request)    

    
    if request.method == 'POST':
        #print("Posted meeting id: "+request.POST.get('meetingID_r'))
        meetingID=request.POST['meetingID_r']
        print("-------------",meetingID)
        options=MeetingEvents.objects.filter(meetingID = meetingID)
        parc=MeetingParticipation.objects.get(meetingID = meetingID ,partID=user.id)
        selected=[]
        if parc.is_voted==True:
            if parc.meetingEventID==None:
                selected=None
            else:    
                selected=parc.meetingEventID.split(',')
                
        print("------Items selected before: ",selected)    
            
   
    #print(options[0].voteNumber)
    ## it should wait for response from the front
      
    
    if request.method == 'POST' and (request.POST.get('ids')!=None):
        print("After POST: ",meetingID)
        requested=request.POST['ids']
        if(requested==''):
            MeetingEventIDs=[]
        else:    
            MeetingEventIDs=(requested).split(',')

        
        ## if a before selected event is unselected
        if len(MeetingEventIDs)==0:
            if parc.is_voted:
                for i in selected:
                    unselected=MeetingEvents.objects.get(meetingEventID = i)
                    unselected.voteNumber-=1
                    unselected.save()
                parc.is_voted=False
                parc.meetingEventID=None
                parc.save()

        else:
            for i in selected:
                if i not in MeetingEventIDs:
                    unselected=MeetingEvents.objects.get(meetingEventID = i)
                    unselected.voteNumber-=1
                    unselected.save()
            parc.meetingEventID=requested
            print(type(MeetingEventIDs))
            for MeetingEventID in MeetingEventIDs:
                if(MeetingEventID not in selected):
                    result=MeetingEvents.objects.get(meetingEventID = MeetingEventID)
                    result.voteNumber+=1
                    result.save()
            parc.is_voted=True
            parc.save()

    totalVote=0
    for option in options:
        print("totalVote",  totalVote)
        totalVote = totalVote + option.voteNumber 
    
    return render(request,'mymeetings/voting.html', {'options': options,'totalVote':totalVote,'meetingID_r':meetingID,'selected':selected})
    
def decide(request):
    user=request.user

    if request.method == 'POST':
            #print("Posted meeting id: "+request.POST.get('meetingID_r'))
            meetingID=request.POST['meetingID_r']
            print("-------------meetingid: ",meetingID)
            options=MeetingEvents.objects.filter(meetingID = meetingID)
            parcs=MeetingParticipation.objects.filter(meetingID = meetingID)
            meeting=Meetings.objects.get(meetingID = meetingID)
            creatorID=meeting.creatorID.id
            print("---Creator id: ",creatorID)
            print("---User id: ",user.id)
            if user.id == creatorID:
                creator=True
            else:
                creator=False

    totalVote=0
    for option in options:
        print("totalVote",  totalVote)
        totalVote = totalVote + option.voteNumber 
          

    if not creator:
        print("-----This is not a creator!!!!")
    else:    
        if request.method == 'POST' and (request.POST.get('ids')!=None):
            print("After POST: ",meetingID)
            MeetingEventID=request.POST['ids']
            #print(type(MeetingEventID))
            meeting.is_decided=True

            result=MeetingEvents.objects.get(meetingEventID = MeetingEventID)
            meeting.start=result.start
            meeting.end=result.end
            meeting.save()

            for parc in parcs:
                finalizeMeeting(parc.partID,meeting,request)


    return render(request,'mymeetings/decide.html', {'options': options,'totalVote':totalVote,'meetingID_r':meetingID})

       
def finalizeMeeting(parcID,meeting,request):

    finalMail(request,parcID,meeting)

    parc=User.objects.get(id=parcID)
    ##
    start=meeting.start
    end=meeting.end

    if(meeting.recurrence == 'single'):
        event=Events(name=meeting.meetingName,start=start,end=end,userID=parc, meetingID = meeting)
        event.save()
    elif(meeting.recurrence == 'weekly'):
        for i in range(3):
            event=Events(name=meeting.meetingName,start=start,end=end,userID=parc, meetingID = meeting)
            event.save()
            start = start + timedelta(7)
            end = end + timedelta(7)
    elif(meeting.recurrence == 'monthly'):
        delta = relativedelta(months=1)
        for i in range(3):
            event=Events(name=meeting.meetingName,start=start,end=end,userID=parc, meetingID = meeting)
            event.save()
            start = start + delta
            end = end + delta
    elif(meeting.recurrence == 'quarterly'):
        delta = relativedelta(months=3)
        for i in range(3):
            event=Events(name=meeting.meetingName,start=start,end=end,userID=parc, meetingID = meeting)
            event.save()
            start = start + delta
            end = end + delta

    ##
    

def finalMail(request,userID,meeting):
    current_site = get_current_site(request)
    
    creator=meeting.creatorID
    user=User.objects.get(id=userID)
    subject = 'We have news for a meeting that you have been invited, created by '+ str(creator.username)+' recurring '+meeting.recurrence+'.'
    message = render_to_string('mymeetings/finalMail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'meeting':  meeting,
                'token': urlsafe_base64_encode(force_bytes(user.password)),
            })
    user.email_user(subject, message)
       

def edit(request):
    if request.method == 'POST':
        meetingID = request.POST['meetingID_r']
        print("----- POST Meeting id: ",meetingID)

    elif request.method == 'GET':   
        meetingID = request.GET.get("meetingID_r", None)
        #meetingID=16
        print("----- GET Meeting id: ",meetingID) 

    meeting=Meetings.objects.get(meetingID=meetingID)

    meetingEvents = MeetingEvents.objects.filter(meetingID = meeting)

    participants = MeetingParticipation.objects.filter(meetingID = meeting)

    partStr=""
    counter = 0
    for part in participants:
        if len(participants)-1 != counter:
            partStr = partStr + str(part.partUsername) + ','
            counter = counter + 1
        else:
            partStr = partStr + str(part.partUsername)

    context = {
        'meeting': meeting,
        'meetingEvents': meetingEvents,
        'participants': partStr,
        'meetingID_r':meetingID
    }
    
    print("Before get")
    
    if request.method == 'GET':
        print("After get")

        name = request.GET.get("meetingName", None)
        print("Meeting name is", name)

        location = request.GET.get("location", None)
        print("Meeting location is", location)

        note = request.GET.get("note", None)
        print("Meeting note is", note)

        

        className = request.GET.get("className", None)
        print("Meeting className is", className)

        
        
        meeting.meetingName=name
        meeting.location=location
        meeting.note=note
        meeting.save()

        if not meeting.is_decided:
            newParticipants = (request.GET.get("participants", None)).split(",")
            newParticipants.append(meeting.creatorID.username)
            print("Meeting participants is", newParticipants)
            recurrence = request.GET.get("recurrence", None)
            print("Meeting recurrence is", recurrence)
            options = request.GET.get("options")
            options = json.loads(options)

            meeting.recurrence=recurrence
            meeting.save()

            ##for removing a participant
            for parc in participants:
                if parc.partUsername not in newParticipants:
                    if parc.meetingEventID != None:
                        MeetingEventIDs=(parc.meetingEventID).split(',')
                    else:
                        MeetingEventIDs=[]
                    print("Delete part: ",parc.partUsername)
                    for MeetingEventID in MeetingEventIDs:
                        votedEvent = MeetingEvents.objects.get(meetingEventID = MeetingEventID)
                        votedEvent.voteNumber-=1
                        votedEvent.save()

                    deletedParticipant(request,meeting,parc)
                    parc.delete()
            participants = MeetingParticipation.objects.filter(meetingID = meeting)
        
            
            ##for adding a participant
            temp=[]
            for i in participants:
                temp.append(i.partUsername)

            print(temp)    
            for newParc in newParticipants:
                if newParc not in temp:
                    newParcUser=User.objects.get(username=newParc)
                    addedParticipant(request,meeting,newParcUser)  ##mail  
                    addedParc=MeetingParticipation(meetingID=meeting,meetingEventID=None,partID=newParcUser.id,partUsername=newParc,is_voted=False)
                    addedParc.save()
            ##for altering options
            meetingIntervals = []
            for i in options:
                start_date = i['start_date']
                start_time = i['start_time']
                total_date = start_date+" "+start_time
                start_date = datetime.strptime(total_date, '%Y-%m-%d %I:%M %p')
                print(start_date)

                end_date = i['end_date']
                end_time = i['end_time']
                total1_date = end_date+" "+end_time
                end_date = datetime.strptime(total1_date, '%Y-%m-%d %I:%M %p')
                print(end_date)

                meetingIntervals.append([start_date, end_date])

            tz = pytz.timezone('Europe/Istanbul')
            optionsChanged=False
            
            for i in range(len(meetingIntervals)):
                optionsChanged=True
                for mEvent in meetingEvents:
                    print("Options test:")
                    
                    start = mEvent.start.astimezone(tz)
                    start=str(start).split('+')[0]
                    end = mEvent.end.astimezone(tz)
                    end=str(end).split('+')[0]
                    print(start)
                    print(meetingIntervals[i][0])
                    if (start == str(meetingIntervals[i][0]) and end == str(meetingIntervals[i][1])):
                            print("Found same")##
                            optionsChanged=False
                            break
                if optionsChanged:
                    break
            participants = MeetingParticipation.objects.filter(meetingID = meeting)            
            if(optionsChanged):
                for parc in participants:
                    changedOpts(request,meeting,parc)
                for mEvent in meetingEvents:
                    print("Event to be deleted",mEvent.meetingEventID)
                    mEvent.delete()
                for meetParc in participants:
                    meetParc.is_voted=False
                    meetParc.meetingEventID=None
                    meetParc.save()
                for i in range(len(meetingIntervals)):
                    newMeetingsEvents = MeetingEvents.objects.create(meetingID = meeting, start=meetingIntervals[i][0],end=meetingIntervals[i][1],voteNumber=0)
                    newMeetingsEvents.save()    

                        

    return render(request,'mymeetings/editMeetingDemo.html', context)

def changedOpts(request,meeting,parc):
    current_site = get_current_site(request)
    
    creator=meeting.creatorID
    user=User.objects.get(id=parc.partID)
    subject = 'We have news for a meeting that you have been invited, created by '+ str(creator.username)+' recurring '+meeting.recurrence+'.'
    message = render_to_string('mymeetings/changedOpts.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'meeting':  meeting,
                'token': urlsafe_base64_encode(force_bytes(user.password)),
            })
    user.email_user(subject, message)
 
def deletedParticipant(request,meeting,parc):
    current_site = get_current_site(request)
    
    creator=meeting.creatorID
    user=User.objects.get(id=parc.partID)
    subject = 'We have news for a meeting that you have been invited, created by '+ str(creator.username)+' recurring '+meeting.recurrence+'.'
    message = render_to_string('mymeetings/removedParc.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'meeting':  meeting,
                'token': urlsafe_base64_encode(force_bytes(user.password)),
            })
    user.email_user(subject, message)
def addedParticipant(request,meeting,parc):
    current_site = get_current_site(request)
    
    creator=meeting.creatorID
    user=parc
    subject = 'You have been added to a meeting created by '+ str(creator.username)+' recurring '+meeting.recurrence+'.'
    message = render_to_string('mymeetings/addedParc.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'meeting':  meeting,
                'token': urlsafe_base64_encode(force_bytes(user.password)),
            })
    user.email_user(subject, message)   

def delete(request):
    meetingID=request.POST['meetingID_r']

    #meeting to be deleted
    meeting = Meetings.objects.get(meetingID = meetingID)

    #this is the current user object
    user = request.user
    #meeting participants to be deleted
    meetingParts = MeetingParticipation.objects.filter(meetingID = meeting.meetingID)
    
    #first send notification emails to the participants
    for i in meetingParts:
        print("current participant:", i.partUsername)
        print("current user:", user.username)
        if i.partUsername != user.username:#only notify participants, not creator
            print("email has been sent to" , i.partUsername)
            partObj = User.objects.get(username = i.partUsername)
            deleteNotification(request, user, i.meetingID, partObj)
    
    #first delete participants
    MeetingParticipation.objects.filter(meetingID = meeting.meetingID).delete()

    #delete meeting events
    MeetingEvents.objects.filter(meetingID = meeting.meetingID).delete()

    #delete actual meeting
    Meetings.objects.filter(meetingID = meetingID).delete()

    #delete meeting's event from calendars
    MeetingEvents.objects.filter(meetingID=meeting).delete()

    return myMeetings(request)
    #return redirect('myMeetings')

def deleteNotification(request, user, meetingInfoObj, partObj):
    current_site = get_current_site(request)

    subject = 'MeetMe: Meeting Deleted by' + ': ' + user.username
    message = render_to_string('mymeetings/deleteNotification.html', {
                'creatorUser': user,
                'partUser': partObj.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(partObj.pk)),
                'meetingInfoObj':  meetingInfoObj,
                'token': urlsafe_base64_encode(force_bytes(partObj.password)),
            })
    partObj.email_user(subject, message)
