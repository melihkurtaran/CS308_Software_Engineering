from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.gCalendar, name="googleApi")
]