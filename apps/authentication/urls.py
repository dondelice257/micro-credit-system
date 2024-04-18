from rest_framework.routers import DefaultRouter

from .views.user import (UserCreationViewSet, UserProfileViewSet,
                         UsersListViewSet)

router = DefaultRouter()

router.register(r'signup', UserCreationViewSet, basename='signup')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'list', UsersListViewSet, basename='list')

urlpatterns = [
    #  path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),

]

urlpatterns += router.urls
