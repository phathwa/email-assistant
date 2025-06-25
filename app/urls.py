from django.urls import path
from . import views

urlpatterns = [
    path('reply/', views.reply_view, name='reply_page'),
    path('compose/', views.compose_view, name='compose_page'),
]