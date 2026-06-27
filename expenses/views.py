from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)    # Only return categories belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related("category")    # Only return expenses belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save