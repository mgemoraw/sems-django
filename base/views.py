from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}

    return render(request, 'base/login_register.html', context=context)


def login(request):
    return None

def logout(request):
    return None 