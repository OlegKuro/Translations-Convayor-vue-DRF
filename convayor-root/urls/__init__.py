from django.contrib import admin
from django.urls import path, include, re_path
from translations.views import SPAView

api_urlpatterns = [

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    re_path(r'.*', SPAView.as_view()),
]
