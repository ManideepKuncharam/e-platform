from django.shortcuts import render

# Create your views here.
def createquiz(request):
    return render(request,'createquiz.html')


def home(request):
    return render(request,'staff.html')