from django.urls import path, include, re_path
from rest_framework import routers

from .views import AccountView, PaymentView, UserViewSet, swagger_conf_view, swagger_index_view

app_name = 'api'

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', UserViewSet, basename='users')
router.register(r'accounts', AccountView, basename='accounts')
router.register(r'payments', PaymentView, basename='payments')

urlpatterns = [
    re_path(r'^$', swagger_index_view, name='swagger_index_view'),
    path('swagger.yaml', swagger_conf_view, name='swagger_conf_view'),
    path('', include(router.urls)),
]
