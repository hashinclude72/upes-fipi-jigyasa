from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserDetails, UserUpdateForm
from .models import User_details
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        user_details_form = UserDetails(request.POST)
        if form.is_valid() and user_details_form.is_valid():
            # form.save()
            user = form.save()
            user.user_details.team_count = user_details_form.cleaned_data.get('team_count')
            user.user_details.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Registered for {username}')
            return redirect('profile')

    else:
        form = UserRegisterForm()
        user_details_form = UserDetails()
    return render(request, 'users/register.html', {'form': form, 'user_details_form':user_details_form , 'title': 'Register'})


# def logout(request):
#     messages.success(request, f'Your account has been logged out.')
#     return redirect('profile')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form  = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')

    else:
        u_form  = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', { 'u_form': u_form, 'title': 'Profile'})
