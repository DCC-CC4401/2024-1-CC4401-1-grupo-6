from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html") 

def register(request):
    return render(request, "register.html")