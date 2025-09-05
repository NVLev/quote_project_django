from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
    path('add/', views.add_quote_view, name='add_quote'),
    path('<int:quote_id>/like/', views.like_quote_view, name='like_quote'),
    path('<int:quote_id>/dislike/', views.dislike_quote_view, name='dislike_quote'),

]