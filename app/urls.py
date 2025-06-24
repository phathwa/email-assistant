from django.urls import path
from . import views

urlpatterns = [
    path('reply/', views.reply_view, name='reply'),
    path('compose/', views.compose_view, name='compose'),
]