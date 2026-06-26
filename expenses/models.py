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
        verbose_name_plural = "categories"  # sets the plural name of the model to "categories" instead of the default "categorys" in admin interface
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],        # same user cannot have duplicate category names
                name="unique_category_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user.email} — {self.name}"