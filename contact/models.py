from datetime import timezone

from django.db import models
from django.forms import EmailField


class Contact(models.Model):
    email = models.EmailField(
        "Email",
        max_length=100,
        unique=True,
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email"
