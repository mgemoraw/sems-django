from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RoomForm

# from .models import Topic

# Create your views here.
def home(request):
    context = {}

    return render(request, 'base/home.html', context=context)

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

def login(request):
    return None

def logout(request):
    return None 