from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_details


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' ,'email' ,'password1', 'password2']


class UserDetails(forms.ModelForm):
    CHOICES=[('1',' 1'),
             ('3',' 3')]
    team_count = forms.ChoiceField(choices=CHOICES, widget=forms.Select)

    class Meta:
        model = User_details
        fields = ['team_count',]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'email']
