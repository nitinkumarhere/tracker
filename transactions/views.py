from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter


class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination

    # Enable filtering and sorting engines
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date', 'amount']  # Allowed sorting fields

    def get_queryset(self):
        # Enforce exact data isolation at the ORM level
        return Transaction.objects.filter(user=self.request.user).select_related('category')
