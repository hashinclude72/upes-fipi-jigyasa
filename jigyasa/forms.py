from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class FeedbackForm(forms.ModelForm):
    from_email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    subject = forms.CharField(label='Subject')
    contact = forms.IntegerField(label='Contact')
    message = forms.CharField(label='Message',widget=forms.Textarea(attrs={'rows':7,'cols':30}))

    class Meta:
        model = User

        fields = ['from_email', 'first_name', 'last_name' ,'subject' ,'contact', 'message']
