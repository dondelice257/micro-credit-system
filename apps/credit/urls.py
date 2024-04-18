from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.credit.views.micro_credit import (MicroCreditCreateView,
                                            MicroCreditViewSet)

router = DefaultRouter()


router.register(r'', MicroCreditViewSet, basename='list')


urlpatterns = [
    path(
        'create/',
        MicroCreditCreateView.as_view(),
        name='microcredit-create'),

]

urlpatterns += router.urls
