from django.urls import path

from authentication.views.home import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    ]