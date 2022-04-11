from django.shortcuts import render


def profile(request):
    return render(request, 'users/profile.html', {'title': 'profile'})


def login(request):
    return render(request, 'users/login.html', {'title': 'login'})


def logout(request):
    return render(request, 'users/logout.html', {'title': 'logout'})
