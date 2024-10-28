from django.urls import path
from . import views

urlpatterns = [
    path('metrics/', views.get_system_info, name='system_metrics'),
]
