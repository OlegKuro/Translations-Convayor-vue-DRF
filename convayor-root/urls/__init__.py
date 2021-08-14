from django.contrib import admin
from django.urls import path, include, re_path

api_urlpatterns = [
    path('translations/', include('translations.urls')),
    path('users/', include('users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
