from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.user import (BanUserView, UserCreationViewSet, UserProfileViewSet,
                         UsersListViewSet)

# Define a DefaultRouter instance
router = DefaultRouter()

# Register viewsets with the router
router.register(r'signup', UserCreationViewSet, basename='signup')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'list', UsersListViewSet, basename='list')

# Define custom paths using Django's path function
urlpatterns = [
    path(
        'ban/',
        BanUserView.as_view(),
        name='ban_user'
    ),
]

# Concatenate the router's generated URLs with custom paths
urlpatterns += router.urls
