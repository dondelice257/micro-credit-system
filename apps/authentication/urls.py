from rest_framework.routers import DefaultRouter
from .views.user import *
from django.urls import path


router = DefaultRouter()


router.register(r'signup', UserCreationViewSet, basename='signup')

urlpatterns = [
    #  path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
     
]

urlpatterns += router.urls




# urlpatterns = router.urls