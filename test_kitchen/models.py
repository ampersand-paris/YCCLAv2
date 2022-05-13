from django.db import models
from accounts.models import CustomUser 

# Create your models here.
class TestKitchenPost(models.Model):
    title = models.CharField(max_length=50, blank=False)
    post = models.CharField(max_length=5000, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title