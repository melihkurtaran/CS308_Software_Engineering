from django.urls import path
from . import views

urlpatterns = [
    path('calendar', views.calendar, name='calendar'),
    path('profile', views.profile, name='profile'),
    path('addmeeting', views.addMeeting, name='addmeeting'),
    path('polls', views.polls, name='polls'),
    path('myMeetings', views.myMeetings, name='myMeetings'),
    path('addEvent', views.addEvent, name='addEvent'),
    path('add_event', views.add_event, name='add_event'),
    path('update', views.update, name='update'),
    path('remove', views.remove, name='remove'),
    path('createMeeting', views.createMeeting, name='createMeeting'),
    path('acceptInvite/<slug:uidb64>/<slug:token>/', views.acceptInvite, name='acceptInvite'),
    path('profileSave', views.profileSave, name='profileSave'),
]
