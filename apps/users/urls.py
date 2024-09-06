from django.urls import path
from apps.users.views.user_views import *


urlpatterns = [
    path('', UserListGenericView.as_view()),
    path('users/', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='register-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
