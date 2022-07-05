from django.urls import path

from .views import rul_politic_list, oppo_politic_list, politic_detail, check_value, likes\
    ,dislikes, delete


app_name = 'politic'

urlpatterns = [
    path('rul_politic_list', rul_politic_list, name='rul_politic_list'),
    path('oppo_politic_list', oppo_politic_list, name='oppo_politic_list'),
    path('<int:id>/<politic_slug>/', politic_detail, name='politic_detail'),
    path('<int:id>/<politic_slug>/api/check-value/', check_value, name='check-value'),
    path('<int:id>/<politic_slug>/like/', likes, name='likes'),
    path('<int:id>/<politic_slug>/dislike/', dislikes, name='dislikes'),
    path('<int:id>/<politic_slug>/<int:pk>/delete', delete, name='dislikes'),
]