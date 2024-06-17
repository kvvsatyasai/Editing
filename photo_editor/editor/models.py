# models.py

from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='images/original/')
    edited_image = models.ImageField(upload_to='images/edited/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
