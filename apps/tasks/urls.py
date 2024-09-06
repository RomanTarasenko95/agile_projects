from django.urls import path
from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView
from apps.tasks.views.task_views import TasksListAPIView, TaskViewListCreateGenericView
from apps.users.views.user_views import UserListGenericView, RegisterUserGenericView, UserDetailView
urlpatterns = [
    path('', TaskViewListCreateGenericView.as_view()),
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
    path('users/', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='register-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
