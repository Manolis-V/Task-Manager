from django.urls import path
from .views import TaskListCreate
from .views import RegisterUser
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', drf_views.obtain_auth_token, name='login'),  # DRF provides this for login
]