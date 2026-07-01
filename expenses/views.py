from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from .permissions import IsOwner  # Import the custom permission class
from .filters import ExpenseFilter
from .pagination import ExpensePagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth

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
    pagination_class = ExpensePagination  # Use the custom pagination class to paginate expenses

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related("category")    # Only return expenses belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save

    @action(detail=False, methods=['get'], url_path='monthly-summary')  # Define a custom action to get monthly summary of expenses
    def monthly_summary(self, request):
        queryset = self.get_queryset()
        data = (
            queryset
            .annotate(month=TruncMonth('expense_date')) # Truncate the expense_date to month to group expenses by month
            .values('month')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('month')
        )
        return Response(data)

    @action(detail=False, methods=['get'], url_path='category-summary')  # Define a custom action to get category summary of expenses
    def category_summary(self, request):
        queryset = self.get_queryset()
        data = (
            queryset
            .values('category__name')
            .annotate(total=Sum('amount'), count=Count('id'), average=Avg('amount'))
            .order_by('-total')
        )
        return Response(data)
    
    @action(detail=False, methods=["get"], url_path="top-spending-categories")  # Define a custom action to get top spending categories of expenses
    def top_spending_categories(self, request):
        limit = int(request.query_params.get("limit", 5))   # Get the limit from query parameters, default to 5 if not provided
        queryset = self.get_queryset()
        data = (
            queryset
            .values("category__id", "category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")[:limit]
        )
        return Response(data)