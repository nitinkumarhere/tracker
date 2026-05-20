from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from decimal import Decimal
import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from transactions.models import Transaction


class AnalyticsDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', description='Filter start date (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='end_date', description='Filter end date (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='months', description='Number of historical months for trend analysis', required=False, type=int, default=6),
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        user = request.user

        # 1. Parse date parameters (default to current year if omitted)
        start_param = request.query_params.get('start_date')
        end_param = request.query_params.get('end_date')
        months_param = request.query_params.get('months', '6')

        today = datetime.date.today()
        start_date = datetime.datetime.strptime(start_param, '%Y-%m-%d').date() if start_param else today.replace(
            month=1, day=1)
        end_date = datetime.datetime.strptime(end_param, '%Y-%m-%d').date() if end_param else today

        base_queryset = Transaction.objects.filter(user=user)
        period_queryset = base_queryset.filter(date__range=[start_date, end_date])

        # 2. Calculate Total Income, Expenses, and Net Balance
        totals = period_queryset.aggregate(
            income=Sum('amount', filter=Q(type='INCOME')),
            expense=Sum('amount', filter=Q(type='EXPENSE'))
        )

        total_income = totals['income'] or Decimal('0.00')
        total_expense = totals['expense'] or Decimal('0.00')
        net_balance = total_income - total_expense

        # 3. Calculate Category Breakdown (Amount + Percentage)
        category_data = period_queryset.filter(type='EXPENSE') \
            .values('category__name') \
            .annotate(amount=Sum('amount')) \
            .order_by('-amount')

        category_breakdown = []
        for item in category_data:
            amt = item['amount'] or Decimal('0.00')
            percentage = (amt / total_expense * 100) if total_expense > 0 else Decimal('0.00')
            category_breakdown.append({
                "category": item['category__name'],
                "amount": amt,
                "percentage": round(float(percentage), 2)
            })

        # 4. Calculate Month-over-Month Summary
        try:
            num_months = int(months_param)
        except ValueError:
            num_months = 6

        # Calculate a threshold date for historical month lookback
        cutoff_date = (today - datetime.timedelta(days=30 * num_months)).replace(day=1)

        historical_data = base_queryset.filter(date__gte=cutoff_date) \
            .annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(
            income=Sum('amount', filter=Q(type='INCOME')),
            expense=Sum('amount', filter=Q(type='EXPENSE'))
        ) \
            .order_by('-month')

        month_summary = []
        for entry in historical_data:
            if entry['month']:
                month_summary.append({
                    "month": entry['month'].strftime('%Y-%m'),
                    "income": entry['income'] or Decimal('0.00'),
                    "expense": entry['expense'] or Decimal('0.00')
                })

        # 5. Build Unified JSON Response Body
        return Response({
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "summary": {
                "total_income": total_income,
                "total_expenses": total_expense,
                "net_balance": net_balance
            },
            "category_breakdown": category_breakdown,
            "month_over_month": month_summary
        })
