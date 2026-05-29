"""
URL configuration for melodix_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# We import path and include from django.urls.
# 'path' helps us define simple routes, and 'include' lets us import other app urls to keep our project organized.
from django.urls import path, include

urlpatterns = [
    # Admin dashboard URL, standard in Django for database management.
    path('admin/', admin.site.urls),
    
    # We prefix all of our music app routes with 'api/'.
    # This means any path inside our music app will be accessed at http://127.0.0.1:8000/api/...
    path('api/', include('music.urls')),
]
