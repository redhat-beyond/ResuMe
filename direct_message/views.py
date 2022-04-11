from django.shortcuts import render


def home(request):
    return render(request, 'direct_message/home.html', {'title': 'direct'})
