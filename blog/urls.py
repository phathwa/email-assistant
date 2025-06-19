from django.urls import path, include

from blog import views

urlpatterns = [
    path('', views.home, name='blog-home'),  # Home page for the blog
    path('about/', views.about, name='blog-about'),  # About page for the blog
]