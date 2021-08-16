from django.urls import path
from users.views import *

app = 'users'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('me', UserMeView.as_view(), name='get_me'),
    path('', UserListCreateView.as_view(), name='users_index_create')
]