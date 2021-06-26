from django.urls import path
from .views import *
urlpatterns =[
    path('', home, name='home'),
    path('home', home),
    path('register', register, name='register'),
    path('login', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('subject', Subjects, name='quiz'),
    path('result', result),

]