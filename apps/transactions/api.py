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
        is_validated = serializer.is_valid()

        if is_validated:
            self.perform_create(serializer)
            data['data'] = serializer.data
            resp_status = status.HTTP_201_CREATED
        else:
            resp_status = status.HTTP_400_BAD_REQUEST
            data['error'] = True
            data['code'] = resp_status
            data['message'] = serializer.errors

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=resp_status, headers=headers)
