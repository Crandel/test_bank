from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response

from transactions.serializers import TransactionDefaultSerializer
from transactions.models import Transaction


class TransactionCreateAPIView(generics.CreateAPIView):
    """
    Available methods:
    - `POST`: Create `Transaction` object.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionDefaultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = {'error': False, 'data': None}

        # check if all data valid and if source_account contains enough money
        is_validated = serializer.is_valid()

        source_account = serializer.validated_data.get('source_account')

        if not is_validated:
            resp_status = status.HTTP_400_BAD_REQUEST
            data['error'] = True
            data['message'] = serializer.errors
        elif source_account and source_account.user != request.user:
            resp_status = status.HTTP_403_FORBIDDEN
            data['error'] = True
            data['message'] = "You don`t have access to this account"
        else:
            self.perform_create(serializer)
            data['data'] = serializer.data
            resp_status = status.HTTP_201_CREATED

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=resp_status, headers=headers)
