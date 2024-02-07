from django.shortcuts import render, redirect
from .models import Students
from .models import Polls
from .models import Sessions
from django import forms
from .forms import SessionForm
from datetime import datetime
now = datetime.now()

#Définir des fonctions

def student_list(request):
    students = Students.objects.all()
    return render(request, 'student_list.html', {'students':students})

def accueil(request):
    return render(request,'accueil.html', context=None)

def sessions(request):
    sessions = Sessions.objects.all()

    #current_date = now.strftime("%d/%m/%Y")
    #current_time = now.strftime("%H:%M:%S")
    #current_datetime = current_date + " " + current_time

    return render(request,'sessions.html', context={'sessions':sessions,})


def create_sessions(request):
    last_session = Sessions.objects.latest('closing_time')
    if request.method == 'POST':
        form = SessionForm(request)
        if form.is_valid():
            form.save()
            return redirect('sessions')
    else:
        form = SessionForm()
    return render(request, 'sessions.html', {'form':form,'last_session':last_session})


def derniers_resultats(request):
    return render(request,'derniers_resultats.html', context=None)