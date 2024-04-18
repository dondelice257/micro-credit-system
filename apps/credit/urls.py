from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.credit.views.micro_credit import (MicroCreditCreateView,
                                            MicroCreditViewSet,
                                            PayCreditView,
                                            ActionToCreditView,
                                            )
from apps.credit.views.micro_credit_type import MicroCreditTypeViewSet
from apps.credit.views.period import PeriodViewSet


router = DefaultRouter()


router.register(r'all', MicroCreditViewSet, basename='list')
router.register(r'type', MicroCreditTypeViewSet, basename='type')
router.register(r'period', PeriodViewSet, basename='type')




urlpatterns = [
    path(
        'create/',
        MicroCreditCreateView.as_view(),
        name='microcredit-create'
        ),

    path(
        'pay/',
        PayCreditView.as_view(),
        name='pay_credit'
        ),

    path(
        'action/',
        ActionToCreditView.as_view(),
        name='action_credit'
        ),



]

urlpatterns += router.urls
