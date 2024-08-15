from django.urls import path, include
from . import views

urlpatterns = [
    #/
    path('', views.home, name='home'),
    #signup/
    path('signup/', views.RegisterUser.as_view(), name='signup_user'),
   
]