from django.db import models
from django.core.validators import MinValueValidator
import random
from django.contrib.auth import get_user_model

User = get_user_model()

class UserStock(models.Model):
    # Link to the default User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # JSONField to store stock names and values as a dictionary
    stocks = models.JSONField()
    custom_id= models.PositiveIntegerField(unique=True, default=random.randint(1000, 9999))
    balance=models.FloatField(default=1000000,validators=[MinValueValidator(0.0)])
    def __str__(self):
        return f"{self.user.username}'s Stock Portfolio"
