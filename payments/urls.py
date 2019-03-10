from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('response/', views.response, name='response'),
    # path('recipt/', views.recipt, name='recipt'),
    path('', views.home, name='home'),
]
