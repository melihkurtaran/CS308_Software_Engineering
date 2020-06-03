from django.urls import path
from . import views

urlpatterns = [
    path('mymeetings', views.myMeetings, name='mymeetings'),
    path('voting',views.voting, name='voting'),
    path('decide',views.decide, name='decide'),
    path('edit',views.edit, name='edit'),
    path('delete',views.delete, name='delete')
]