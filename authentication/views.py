from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserProfileSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    # def update(self, request, *exclude_kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid = serializer.is_valid(raise_exception=True)
    #
    #     request.user.set_password(serializer.validated_data['new_password'])
    #     request.user.save()
    #     return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Fixed the typo here

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

