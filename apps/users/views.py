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
        import ipdb; ipdb.set_trace()  # BREAKPOINT
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_dict = UserSerializer(context={'request': request}, instance=user)
        return Response(user_dict.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
