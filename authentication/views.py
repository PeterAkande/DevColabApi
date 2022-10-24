from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import UserCreationSerializer, UserSiginSerializer


def get_token(user_instance):
    # Function to create a token for the newly created user
    token = Token.objects.get_or_create(user=user_instance)

    return token[0].key


class UserCreationView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_token(user)

            return Response(data={'user-details': serializer.data, 'token': token}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_creation_view = UserCreationView.as_view()


class UserSignInView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSiginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=data['email'], password=data['password'])
    
        if user:
            user.check_password(data['password'])
            token = get_token(user)

            return Response(data={'token': token}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'error': 'account not found, email or password not correct'},
                        status=status.HTTP_400_BAD_REQUEST)


user_signin_view = UserSignInView.as_view()


class ResetPasswordView(generics.GenericAPIView):
    # TODO: Add this view
    pass

