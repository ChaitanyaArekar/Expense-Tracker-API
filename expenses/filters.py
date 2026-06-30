import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    expense_date_after = django_filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    expense_date_before = django_filters.DateFilter(field_name="expense_date", lookup_expr="lte")

    class Meta:
        model = Expense
        fields = ["category", "expense_date", "min_amount", "max_amount"]