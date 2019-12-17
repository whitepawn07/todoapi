from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class List(models.Model):
    """
    a model for creating a list of a user
    """

    Priority_Choices = [
        ('lp',"Low Priority"),
        ('mp',"Medium Priority"),
        ('hp',"High Priority")
    ]

    title = models.CharField(max_length=150,default="")
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    priority = models.CharField(max_length=2, choices=Priority_Choices, default='lp')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
