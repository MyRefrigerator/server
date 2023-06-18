from django.urls import include, path

from .expired_ingredient_alarm_controller import ExpiredIngredientAlarmController

urlpatterns = [
    path('expired-ingredient', ExpiredIngredientAlarmController.as_view(), name='url-name'),
]