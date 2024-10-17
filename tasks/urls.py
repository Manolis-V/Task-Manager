from django.urls import path
from .views import TaskListCreate, RegisterUser, UserListView, TaskDetailUpdateDelete
#TaskDetail, 
urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('tasks/<int:pk>/', TaskListCreate.as_view(), name='task-update'),
    # path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:pk>/', TaskDetailUpdateDelete.as_view(), name='task-detail-update-delete'),
    path('users/', UserListView.as_view(), name='user-list'),
]