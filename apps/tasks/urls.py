from django.urls import path
from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView
from apps.tasks.views.task_views import TasksListAPIView, TaskViewListCreateGenericView, TaskDetailAPIView
from apps.users.views.user_views import UserListGenericView, RegisterUserGenericView, UserDetailView

urlpatterns = [
    path('tasks/', TaskViewListCreateGenericView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),
    path('users/', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='register-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
