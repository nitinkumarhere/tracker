from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_default']
        read_only_fields = ['id', 'is_default']

    def create(self, validated_data):
        # Automatically assign the logged-in user to the custom category
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
