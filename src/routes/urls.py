from django.urls import include, path

urlpatterns = [
    path('api/v1/', include('src.routes.v1_urls'))
]