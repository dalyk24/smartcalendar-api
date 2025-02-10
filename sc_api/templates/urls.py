from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.test_view),
    path('api/new_user', views.new_user),
    path('api/new_task', views.new_task, name='new_task'),
    path('api/update_task', views.update_task),
    path('api/delete_task', views.delete_task),
    path('api/get_tasks', views.get_tasks),
    path('api/evaluate_task', views.evaluate_task),
]
