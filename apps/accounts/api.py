from django.http import Http404
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from accounts.serializers import (
    AccountDetailSerializer, AccountDefaultSerializer, AccountListSerializer
)
from accounts.models import Account


class AccountCreateAPIView(generics.CreateAPIView):
    """
    Available methods:
    - `POST`: Create `Account` object.
    """
    queryset = Account.objects.all()
    serializer_class = AccountDefaultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        serializer = self.get_serializer(data=request.data)
        data = {'error': False, 'data': None}
        is_validated = serializer.is_valid()
        if is_validated:
            self.perform_create(serializer)
            resp_status = status.HTTP_201_CREATED
            data['data'] = serializer.data
        else:
            resp_status = status.HTTP_400_BAD_REQUEST
            data['error'] = True
            data['code'] = resp_status
            data['message'] = serializer.errors

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=resp_status, headers=headers)


class AccountDetailAPIView(generics.RetrieveAPIView):
    """
    Available methods:
    - `GET`: Getting detail information about `Account` object for all authenticated users.
    """
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "pk"

    def retrieve(self, request, *args, **kwargs):
        data = {'error': False, 'data': None}

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data['data'] = serializer.data
        except Http404 as e:
            data['error'] = True
            data['code'] = status.HTTP_404_NOT_FOUND
            data['message'] = str(e)
        return Response(data)


class AccountListAPIView(generics.ListAPIView):
    """
    Available methods:
    - `GET`: Getting list of `Account` objects for all authenticated users
    """
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AccountListSerializer(queryset, many=True)
        data = {
            'error': False,
            'data': serializer.data
        }
        return Response(data)
