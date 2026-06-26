from .models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        value = value.strip().title()  # so Food ,FOOD and food are treated as the same category Food.
        if not value:
            raise serializers.ValidationError("Category name cannot be empty.")
        return value