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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_validated = serializer.is_valid()

        if is_validated:
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user_dict = UserSerializer(context={'request': request}, instance=user)
            data = {'errors': False, 'data': user_dict.data}
        else:
            data['error'] = True
            data['code'] = status.HTTP_400_BAD_REQUEST
            data['message'] = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
