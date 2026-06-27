from .models import Category, Expense
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
    
class CategorySummarySerializer(serializers.ModelSerializer):   # to get category details in the expense response of expense serializer
    class Meta:
        model = Category
        fields = ["id", "name"]

class ExpenseSerializer(serializers.ModelSerializer):
    category_details = CategorySummarySerializer(source="category", read_only=True)  # nested serializer to include category details in the expense response
    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "expense_date", "notes", "category", "category_details", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Expense title cannot be empty.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value
    
    def validate_category(self,value):
        request = self.context. get("request")
        if  value.user != request.user:
            raise serializers.ValidationError("You can only assign expenses to your own categories.")
        return value