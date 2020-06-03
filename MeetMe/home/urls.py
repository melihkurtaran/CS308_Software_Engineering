from django.urls import path
from . import views


#from .views import login

urlpatterns = [
    path("", views.home, name="home"),
    #path('login/',include('accounts.urls',namespace="login")),
    #path('login/', views.login, name="login")
    #path("upper_menu", views.upper_menu, name="upper_menu")
]
