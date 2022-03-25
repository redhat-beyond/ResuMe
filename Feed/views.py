from django.shortcuts import render


def resumeApp(request):
    return render(request, 'Feed/index.html')
