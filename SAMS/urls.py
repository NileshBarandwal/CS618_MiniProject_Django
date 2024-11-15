from django.contrib import admin
from django.urls import path, include  # include is used to reference the app's urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sams.urls')),  # This includes the 'sams' app URLs
    path('auth/', include('django.contrib.auth.urls')),  # Built-in authentication view
    path('', include('frontend.urls')),  # Include frontend app routes
]