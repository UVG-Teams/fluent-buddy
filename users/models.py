from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tema(models.Model):
    user = models.ForeignKey(
        User,
        null = False,
        on_delete = models.CASCADE,
    )
    tema = models.CharField(
        max_length = 100,
        null = False,
    )

    def __str__(self):
        return self.tema
