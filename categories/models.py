from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        # Prevent a user from creating duplicate categories of the same name
        unique_together = ('name', 'user')

    def __str__(self):
        return f"{self.name} (Default)" if self.is_default else f"{self.name} ({self.user.email})"
