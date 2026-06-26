from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)    # Only return categories belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)     # Automatically attach the logged-in user to user field on save