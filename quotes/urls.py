from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
    path('add/', views.add_quote_view, name='add_quote')

]