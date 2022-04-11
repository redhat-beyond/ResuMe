from django.shortcuts import render


def feed(request):
    return render(request, 'posts/feed.html', {'title': 'feed'})


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


def search(request):
    return render(request, 'posts/search.html', {'title': 'search'})
