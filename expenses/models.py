from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories"       # allows reverse lookup of categories for a user instead of using category_set.all() we use user.categories.all()
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"  # sets the plural name of the model to "categories" instead of the default "categorys" in admin interface
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],        # same user cannot have duplicate category names
                name="unique_category_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user.email} — {self.name}"

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"           # allows reverse lookup of expenses for a user instead of using expense_set.all() we use user.expenses.all()
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # prevents deletion of a category if it is associated with any expenses
        related_name="expenses"           # allows reverse lookup of expenses for a category instead of using expense_set.all() we use category.expenses.all()
    )
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expense_date", "-created_at"]
        verbose_name_plural = "Expenses"  # sets the plural name of the model to "expenses" instead of the default "expenses" in admin interface

    def __str__(self):
        return f"{self.user.email} — {self.title} — {self.amount}"