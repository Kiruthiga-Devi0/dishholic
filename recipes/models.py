from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()

    steps = models.JSONField(
        help_text="List of steps for holographic simulation"
    )

    duration = models.IntegerField(default=0)

    difficulty = models.CharField(
        max_length=20,
        choices=[('Easy','Easy'), ('Medium','Medium'), ('Hard','Hard')],
        default='Easy'
    )

    
    image_url = models.URLField(blank=True, null=True)

    favorites = models.ManyToManyField(User, related_name="favorite_recipes", blank=True)

    def __str__(self):
        return self.name