import re
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.fields import empty

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'weak_password': _('Password must be 8-16 characters, with at least 1 digit.')
    }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value):
        """
        Validation of password
        """
        password = value
        regex = re.compile("^(?=.*\d)(?=.*[a-zA-z]).{8,16}$")
        if not regex.match(password):
            raise serializers.ValidationError(self.default_error_messages['weak_password'])
        return value


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'token')

    def __init__(self, instance=None, data=empty, **kwargs):
        self.fields['password'].write_only = True
        super().__init__(instance, data, **kwargs)

    def get_token(self, obj):
        return obj.get_token

    def save(self, **kwargs):
        new_password = self.validated_data.get('password')
        user = super(UserSerializer, self).save(**kwargs)
        if new_password:
            user.set_password(new_password)
            user.save()
        return user
