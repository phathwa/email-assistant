from django.contrib import admin
from django.urls import path, include

from emailassistant.view import landing_page

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('', include('app.urls')),  # Include the app URLs with a blank prefix
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Add 'api/' prefix here
    # Include the blog app URLs with a 'blog/' prefix
    path('blog/', include('blog.urls')),  # Add 'blog/' prefix here

]
