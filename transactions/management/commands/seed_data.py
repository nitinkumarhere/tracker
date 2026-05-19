from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from transactions.models import Transaction
import random
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with a test user and fake transaction history'

    def handle(self, *args, **options):
        # 1. Create or fetch a demo user
        user, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={'name': 'Demo User'}
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS("Created user: demo@example.com (password: password123)"))

        # 2. Fetch seeded system default categories
        categories = list(Category.objects.filter(is_default=True))
        if not categories:
            self.stdout.write(self.style.ERROR("Please run 'python manage.py seed_categories' first!"))
            return

        # 3. Generate random historical entries spanning the last 90 days
        today = datetime.date.today()
        transaction_types = ['INCOME', 'EXPENSE']
        notes = ["Salary payout", "Weekly groceries", "Electric bill", "Coffee run", "Uber ride", "Flight ticket",
                 "Movie night"]

        count = 0
        for i in range(100):
            days_ago = random.randint(0, 90)
            tx_date = today - datetime.timedelta(days=days_ago)
            tx_type = random.choice(transaction_types)

            if tx_type == 'INCOME':
                amount = round(random.uniform(500, 3000), 2)
                # Assign to 'Other' or a general category for simplicity
                category = Category.objects.get(name='Other', is_default=True)
            else:
                amount = round(random.uniform(5, 150), 2)
                category = random.choice(categories)

            Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                type=tx_type,
                date=tx_date,
                note=random.choice(notes)
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} historical financial entries!"))
