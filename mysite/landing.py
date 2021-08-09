from django.shortcuts import render

def landingView(request):
    return render(request,'landingpage/index.html')