from django.urls import include, path

from .server_status_controller import ServerStatusController
from .app_version_status_controller import AppVersionStatusController

urlpatterns = [
    path('server', ServerStatusController.as_view(), name='url-name'),
    path('app-version', AppVersionStatusController.as_view(), name='url-name')
]