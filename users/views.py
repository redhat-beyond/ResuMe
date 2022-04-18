from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'profile'})


def login(request):
    return render(request, 'users/login.html', {'title': 'login'})


def logout(request):
    return render(request, 'users/logout.html', {'title': 'logout'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit-profile.html', context)
