from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def vprofile(request):

    context = {
        
    }
    return render(request,'vendor/vprofile.html',context)