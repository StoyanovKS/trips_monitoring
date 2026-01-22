from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class CurrencyChoices(models.TextChoices):
        BGN = "BGN", "BGN"
        EUR = "EUR", "EUR"

    preferred_currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.BGN,
    )

    timezone = models.CharField(
        max_length=64,
        default="Europe/Sofia",
    )

    def __str__(self):
        return self.username
