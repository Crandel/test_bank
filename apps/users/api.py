from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, status
from rest_framework.response import Response

from users.serializers import SignUpSerializer, UserSerializer

User = get_user_model()


class SignUpView(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Api endpoint for registration.
        email - should be unique
        password - must be 8-16 characters, with at least 1 digit.
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_validated = serializer.is_valid()
        data = {'errors': False, 'data': []}
        if is_validated:
            user = self.perform_create(serializer)
            user_dict = UserSerializer(context={'request': request}, instance=user)
            data['data'] = user_dict.data
            resp_status = status.HTTP_201_CREATED
        else:
            resp_status = status.HTTP_400_BAD_REQUEST
            data['error'] = True
            data['code'] = status.HTTP_400_BAD_REQUEST
            data['message'] = serializer.errors

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=resp_status, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
