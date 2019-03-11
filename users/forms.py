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
    team_count = forms.TypedChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'style': 'display: inline-block'}))
    contact_no = forms.IntegerField()

    class Meta:
        model = User_details
        fields = ['team_count','contact_no',]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'email']


class ContactUpdateForm(forms.ModelForm):
    contact_no = forms.IntegerField(required=False)

    class Meta:
        model = User_details
        fields = ['contact_no',]
