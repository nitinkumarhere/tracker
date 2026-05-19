import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'start_date', 'end_date']
