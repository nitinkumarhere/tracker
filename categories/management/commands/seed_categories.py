from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = 'Seeds the database with default system categories'

    def handle(self, *args, **options):
        default_categories = [
            'Food', 'Transport', 'Bills', 'Health',
            'Shopping', 'Travel', 'Leisure', 'Other'
        ]

        for name in default_categories:
            category, created = Category.objects.get_or_create(
                name=name,
                is_default=True,
                user=None
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {name}"))
