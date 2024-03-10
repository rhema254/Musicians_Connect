from django.urls import path
from .views import *

urlpatterns = [
path('basehtmltrial/', basehtmltrial, name='basehtmltrial'),
]