from django.urls import path
from . import views

urlpatterns = [
    path('paytm/', views.paytm, name='paytm'),
    path('response/', views.response, name='response'),
    path('recipt/', views.recipt, name='recipt'),
    path('', views.payments_home, name='payments_home'),
]
