from django.urls import path

from . import views

urlpatterns = [
    # /display/
    path('', views.index, name='index'),
]
