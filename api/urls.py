from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='api-home'),
    path('generate-reply/', views.generate_reply, name='generate_reply'),
    path('generate-compose/', views.generate_compose, name='generate_compose'),  # ✅ Add this

]
