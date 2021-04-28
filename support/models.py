from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(
        User,
        null = False,
        on_delete = models.CASCADE,
    )
    message = models.CharField(
        max_length = 500,
        null = False
    )

    def __str__(self):
        return self.message