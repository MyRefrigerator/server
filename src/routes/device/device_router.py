from django.urls import include, path

from .device_registration_controller import DeviceRegistrationController

urlpatterns = [
    path('/registration', DeviceRegistrationController.as_view(), name='url-name'),
]