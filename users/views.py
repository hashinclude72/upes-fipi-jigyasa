from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserDetails, UserUpdateForm, ContactUpdateForm
from .models import User_details
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.sessions.models import Session
from payments.models import Paytm_history

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        user_details_form = UserDetails(request.POST)
        if form.is_valid() and user_details_form.is_valid():
            # form.save()
            user = form.save()
            user.user_details.team_count = user_details_form.cleaned_data.get('team_count')
            user.user_details.contact_no = user_details_form.cleaned_data.get('contact_no')
            user.user_details.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Registered for {username}')
            return redirect('profile')

    else:
        form = UserRegisterForm()
        user_details_form = UserDetails()
    return render(request, 'users/register.html', {'form': form, 'user_details_form':user_details_form , 'title': 'Register'})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form  = UserUpdateForm(request.POST, instance=request.user)
        contact_u_form = ContactUpdateForm(request.POST, instance=request.user.user_details)
        if u_form.is_valid() and contact_u_form.is_valid():
            u_form.save()
            contact_u_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')

    else:
        u_form  = UserUpdateForm(instance=request.user)
        contact_u_form = ContactUpdateForm(instance=request.user.user_details)

    user = request.user
    status = False
    if Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS'):
        status = True
    return render(request, 'users/profile.html', { 'u_form': u_form, 'contact_u_form':contact_u_form, 'title': 'Profile'})
