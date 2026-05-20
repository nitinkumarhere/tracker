from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Return all system defaults PLUS categories created by the logged-in user
        return Category.objects.filter(
            Q(is_default=True) | Q(user=self.request.user)
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.is_default:
            raise PermissionDenied("Default categories cannot be updated.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.is_default:
            raise PermissionDenied("Default categories cannot be deleted.")
        instance.delete()
