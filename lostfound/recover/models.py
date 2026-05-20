from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):

  STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('CLAIMED', 'Claimed'),
    ]

  title = models.CharField(max_length=255)
  description = models.TextField()
  image = models.ImageField(upload_to='items/', blank=True, null=True)
  location = models.CharField(max_length=255)

  status = models.CharField(max_length=10, choices=STATUS_CHOICES)
  lost_date=models.DateField(null=True, blank=True)
  found_date=models.DateField(null=True, blank=True)
  is_approved=models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
        return self.title
class Claim(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
  
    message = models.TextField()
    contact = models.CharField(max_length=100)

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}-{self.item}" 