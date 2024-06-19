from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .models import Message, Chat
from django.contrib.auth.decorators import login_required

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