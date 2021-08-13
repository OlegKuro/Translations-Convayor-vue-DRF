from django.urls import path
from user.views import *

app = 'user'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('me', UserMeView.as_view(), name='get_me'),
]