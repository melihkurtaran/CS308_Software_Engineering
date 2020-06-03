from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name= 'accounts/logout.html'), name= 'logout'),
    path('logout/', views.logout, name= 'logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('gLogin/',include('allauth.urls')),
    #auth_views.login.as_view(template_name= 'users/login.html')path('logout/', auth_views.LogoutView.as_view(template_name= 'users/logout.html'), name= 'logout')
]
