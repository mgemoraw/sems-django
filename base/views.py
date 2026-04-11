from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from api.models import User
import csv

from .forms import RoomForm, UserRegisterForm

# from .models import Topic

# Create your views here.
def home(request):
    # exams = Exam.objects.all()
    users = User.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'base/home.html', context=context)

def dashboard(request):
    context = {}
    return render(request, 'base/dashboard.html', context=context)

def admin_users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'base/admin_users.html', context=context)


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


def user_delete(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully")
    else:
        messages.error(request, f"User '{username}' not found")
    return redirect('base:home')

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not username or not password:
            messages.error(request, "Username and password are required")
            return redirect("base:dashboard")

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.email = email
            user.set_password(password)
            user.is_staff = True if role == "admin" else False
            user.save()
            messages.success(request, f"User '{username}' created successfully")
        else:
            messages.error(request, f"User '{username}' already exists")

    return redirect("base:dashboard")

def edit_user(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        messages.error(request, f"User '{username}' not found")
        return redirect("base:dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user.email = email
        if password:
            user.set_password(password)
        user.is_staff = True if role == "admin" else False
        user.save()
        messages.success(request, f"User '{username}' updated successfully")

    return redirect("base:dashboard")

def bulk_users(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        default_role = request.POST.get("default_role")
        overwrite = request.POST.get("overwrite")

        if not file.name.endswith(".csv"):
            messages.error(request, "Invalid file format")
            return redirect("base:dashboard")

        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0

        for row in reader:
            username = row.get("username")
            email = row.get("email")
            password = row.get("password")
            role = row.get("role") or default_role

            if not username or not password:
                continue

            user, created = User.objects.get_or_create(username=username)

            if created or overwrite:
                user.email = email
                user.set_password(password)
                user.is_staff = True if role == "admin" else False
                user.save()
                created_count += 1

        messages.success(request, f"{created_count} users uploaded successfully")
        return redirect("base:dashboard")