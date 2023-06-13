from django.contrib import admin
from django.urls import path

from .basic.basic_controller import BasicView

urlpatterns = [
    path('admin/', BasicView.as_view(), name='url-name'),
]
