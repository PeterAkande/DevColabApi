from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    last_name = serializers.CharField(max_length=25)
    first_name = serializers.CharField(max_length=25)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'last_name', 'first_name', 'password']

    def validate(self, attrs):
        username_exists = CustomUser.objects.filter(username=attrs['username']).exists()
        if username_exists:
            raise serializers.ValidationError(_('Username Exists. Please use another username'))

        email_exists = CustomUser.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(_('Email address Exists. Please use another email address'))

        return super().validate(attrs)

    def save(self, **kwargs):
        # This function is to further save the user password since we require it to be hashed

        user = super().save(**kwargs)
        user.set_password(user.password)
        user.save()

        return user


class UserSiginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=80, )
    password = serializers.CharField(min_length=8)

    class Meta:
        fields = ['email', 'password',]
