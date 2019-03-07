from django.shortcuts import render

def home(request):
    return render(request, 'jigyasa/home.html')


def about(request):
    return render(request, 'jigyasa/about.html', {'title': 'About'})

def events(request):
    return render(request, 'jigyasa/events.html', {'title': 'Events'})

def gallery(request):
    return render(request, 'jigyasa/gallery.html', {'title': 'Gallery'})

def contacts(request):
    return render(request, 'jigyasa/contacts.html', {'title': 'Contacts'})
