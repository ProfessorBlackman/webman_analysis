from django.urls import path

from authentication.views.authentication import SignUpView, LoginView
from authentication.views.home import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    ]