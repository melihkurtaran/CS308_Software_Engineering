from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#this stores every user's events on their calendar

#data entered here when a meeting is created by the user
class Meetings(models.Model):
    meetingID = models.AutoField(primary_key=True)
    meetingName = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    participants = models.CharField(max_length=255, null=True, blank=True)
    recurrence = models.CharField(max_length=255, null=True, blank=True)
    is_decided = models.BooleanField(default=False)
    creatorID = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    """
    beginLimit = models.DateTimeField(null=True)
    endLimit = models.DateTimeField(null=True)
    meetingDuration = models.CharField(max_length=255, null=True, blank=True)
    """
class Events(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
class MeetingEvents(models.Model):
    meetingEventID = models.AutoField(primary_key=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    voteNumber = models.IntegerField(null=True)
"""
class MeetingsAttendance(models.Model):
    meetingAttID = models.AutoField(primary_key=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    partID = models.IntegerField(null=True)
    partUsername = models.CharField(max_length=255, null=True, blank=True)
    is_voted = models.BooleanField(default=False)
"""
class invitedMeetingList(models.Model):
    invitedMeetingID = models.AutoField(primary_key=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    participantID = models.IntegerField(null=True)

#this is to record the users and the participation of a recorded meeting
class MeetingParticipation(models.Model):
    meetingParID = models.AutoField(primary_key=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    meetingEventID = models.CharField(max_length=255, null=True, blank=True)
    partID = models.IntegerField(null=True)
    partUsername = models.CharField(max_length=255, null=True, blank=True)
    #attendance = models.BooleanField(default=False)
    is_voted = models.BooleanField(default=False)



"""
#this is to store the computed possible meeting time frame for a meeting
class Meetings_Computed(models.Model):
    meetingCompID = models.AutoField(primary_key=True)
    meetingID =  models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    meetingIsActive = models.BooleanField(default=False)
    computedStart = models.DateTimeField(null=True)
    computedEnd = models.DateTimeField(null=True)
"""