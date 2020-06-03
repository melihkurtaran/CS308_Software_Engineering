from django.shortcuts import render
from django.views.generic import ListView, DetailView


def home(request):
    return render(request,'home/index.html')

#class HomeView(DetailView):
#    template_name = 'home/index.html'
    #return render(request,'home/index.html')



#class LoginView(DetailView):
    #model = accounts
#    template_name = 'accounts/login.html'
