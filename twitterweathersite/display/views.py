from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    context = {}
    return render(request, 'display/dashboard.html', context)
