from django.shortcuts import render, redirect
from .models import Usuario


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def publicar(request):
    return render(request, "publicar.html")


def register(request):
    return render(request, "register.html")


def test(request):
    if request.method == "GET":
        return render(request, "test_form.html")
    if request.method == "POST":
        data = request.POST
        user = Usuario(
            username=data.get("username"),
            name=data.get("name"),
            password=data.get("password_section"),
            email=data.get("email"),
        )
        user.save()
        return render(request, "test_items.html", {"data": data})
