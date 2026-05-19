from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']  # Default sorting: newest records first

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.user.email})"
