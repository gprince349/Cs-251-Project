from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    val = 'ashish'
    return render(request, 'home.html',{'alexa':val})


def add(request):
     val1 = request.POST["num1"]
     val2 = request.POST["num2"]

     val3 = int(val1) + int(val2)

     return render(request, 'result.html', {'result' : val3})

