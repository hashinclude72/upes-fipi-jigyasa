from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='jigyasa-home'),
    path('about/', views.about, name='jigyasa-about'),
    path('events/', views.events, name='jigyasa-events'),
    path('gallery/', views.gallery, name='jigyasa-gallery'),
    path('contacts/', views.contacts, name='jigyasa-contacts'),
]
