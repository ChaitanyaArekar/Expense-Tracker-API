from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from .permissions import IsOwner  # Import the custom permission class
from .filters import ExpenseFilter

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]  # Use the custom permission class to ensure only owners can access their categories

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)    # Only return categories belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsOwner]  # Use the custom permission class to ensure only owners can access their expenses
    filterset_class = ExpenseFilter  # Use the custom filter class to filter expenses based on query parameters
    search_fields = ['title', 'notes']  # Allow searching expenses by title and notes
    ordering_fields = ['amount', 'expense_date', 'created_at']  # Allow ordering expenses by amount, expense_date and created_at
    ordering = ['-expense_date']    # Set default ordering of expenses by expense_date in descending order

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related("category")    # Only return expenses belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save 