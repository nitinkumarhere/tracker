from rest_framework import serializers
from .models import Transaction
from categories.models import Category
from django.db.models import Q

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'category_name', 'date', 'note']
        read_only_fields = ['id']

    def validate_category(self, value):
        user = self.context['request'].user
        # Verify the chosen category belongs to the user or is a system default
        if not value.is_default and value.user != user:
            raise serializers.ValidationError("You do not have permission to use this category.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
