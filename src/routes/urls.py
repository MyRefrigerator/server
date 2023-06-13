from django.urls import include, path
from .basic_view import BasicView

urlpatterns = [
    path('', BasicView.as_view(), name='url-name'),
    path('api/v1/', include('src.routes.v1_urls'))
]