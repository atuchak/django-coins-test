from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.response import Response

from billing.models import Account, Payment
from .serializers import UserSerializer, AccountSerializer, PaymentSerializer

from django.contrib.auth import get_user_model

UserModel = get_user_model()


def swagger_index_view(request):
    return render(request, 'api/swagger.html')


def swagger_conf_view(request):
    return render(request, 'api/swagger.yaml')


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for UserModel.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class AccountView(viewsets.GenericViewSet):
    """
    This viewset  provides `list`, `create` actions for Account model.
    """
    serializer_class = AccountSerializer
    queryset = Account.objects

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class PaymentView(viewsets.GenericViewSet):
    """
    This viewset  provides `list`, `create` actions for Payment model.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
