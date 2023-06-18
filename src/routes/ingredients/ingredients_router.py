from django.urls import include, path

from .ingredients_controller import IngredientsController
from .ingredients_sample_controller import IngredientsSampleController

from .ingredients_auto_input_controller import IngredientsAutoInputController
from .ingredients_manual_input_controller import IngredientsManualInputController

urlpatterns = [
    path('', IngredientsController.as_view(), name='url-name'),
    path('sample', IngredientsSampleController.as_view(), name='url-name'),
    path('auto-input', IngredientsAutoInputController.as_view(), name='url-name'),
    path('manual-input', IngredientsManualInputController.as_view(), name='url-name')
]