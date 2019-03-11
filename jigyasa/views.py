from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import FeedbackForm
from django.views.decorators.csrf import csrf_exempt
import os

def home(request):
    return render(request, 'jigyasa/home.html')


def about(request):
    return render(request, 'jigyasa/about.html', {'title': 'About'})

def events(request):
    return render(request, 'jigyasa/events.html', {'title': 'Events'})

def gallery(request):
    return render(request, 'jigyasa/gallery.html', {'title': 'Gallery'})


@csrf_exempt
def contacts(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            subject = feedback_form.cleaned_data.get('subject')
            message = feedback_form.cleaned_data.get('message')
            from_email = feedback_form.cleaned_data.get('from_email')
            first_name = feedback_form.cleaned_data.get('first_name')
            last_name = feedback_form.cleaned_data.get('last_name')
            contact = feedback_form.cleaned_data.get('contact')

            msg_mail = "Name :- " + str(first_name) + " " + str(last_name) + "\n\nFrom Email :- " + str(from_email) + "\n\nConatct :- " + str(contact) + "\n\n" + "Message :- \n" + str(message)
            #+ "Message :- \n"
            try:
                send_mail(subject, msg_mail, from_email, [os.environ.get('EMAIL_USER'), 'rockgameplayer@gmail.com', from_email], fail_silently = False)
                messages.success(request, f'Feedback sent.')
            except BadHeaderError:
                messages.success(request, f'Feedback sending failed.')
            return redirect("jigyasa-contacts")

    feedback_form = FeedbackForm()
    return render(request, 'jigyasa/contacts.html', {'feedback_form':feedback_form , 'title': 'Contacts'})
