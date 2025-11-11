from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('create/', views.room_create, name='room_create'),
    path('room/<slug:slug>/', views.room_detail, name='room_detail'),
]