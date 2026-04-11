from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RoomForm, UserRegisterForm

# from .models import Topic

# Create your views here.
def home(request):
    
    context = {
        
    }

    return render(request, 'base/home.html', context=context)

def dashboard(request):
    context = {}
    return render(request, 'base/dashboard.html', context=context)


def room(request, pk):
    context = {}

    return redirect('base:home')


def exam(request):
    context = {}

    return redirect('base:home')

def results(request):
    context = {}

    return redirect('base:home')

def bulk_upload(request):
    context = {}

    return redirect('base:home')

def profile(request):
    context = {}
    return redirect('base:home')

@login_required(login_url='base:login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # assign creator
            room.save()
            return redirect('base:home')

    context = {'form': form}
    return render(request, 'base/create_room.html', context)

    # if form.is_valid():
    #     topic_name = request.POST.get('topic')
    #     topic, created = Topic.objects.get_or_create(name=topic_name)

    #     room = form.save(commit=False)
    #     room.host = request.user
    #     room.topic = topic
    #     room.save()

    #     return redirect('base:home')

def user_register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base:home')
    context = {'page': 'register', 'form': form}  
    return render(request, 'base/login_register.html', context = context)

def user_login(request):
    # If the user is already logged in, send them to the dashboard/home
    if request.user.is_authenticated:
        return redirect('base:home') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate checks if the credentials match a user in the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')  # Change 'home' to your desired redirect URL
        else:
            messages.error(request, 'Invalid username or password')

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)

def user_logout(request):
    logout(request)
    return redirect('base:home')