from django.urls import path, include

urlpatterns = [
    path('status', include('src.routes.status.status_router')),
    path('alarm', include('src.routes.alarm.alarm_router')),
    path('device', include('src.routes.device.device_router')),
    path('ingredients', include('src.routes.ingredients.ingredients_router')),
]
