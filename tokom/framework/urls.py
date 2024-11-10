from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tokom.urls', namespace='tokom')),
    path('auth/', include('auth_app.urls', namespace='auth_app')),
    
]
