from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView, UserEdit

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserEdit.as_view(), name='me'),
]
