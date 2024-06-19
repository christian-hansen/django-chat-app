from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    
    if request.method == 'POST':        
        print("Request method is post")      
        print(request.POST['textmessage'])   
        myChat = Chat.objects.get(id=1) 
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    chat_messages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'chat_messages': chat_messages})

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect (request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True}, {'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    if request.method == 'POST':
        print("Request method is post")        
        user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            # wenn User registriert login und Weiterleitung zu /chat
            login(request, user)
            redirectToChat = redirect('/chat/')
            return redirectToChat
        else:
            return render(request, 'auth/register.html', {'error': True})
        # wenn passwörter nicht gleich, fehler
    return render(request, 'auth/register.html')