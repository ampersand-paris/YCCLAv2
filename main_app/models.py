from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = ArrayField(models.CharField(max_length=100)) 
    preparation = ArrayField(models.CharField(max_length=1000)) 

    def __str__(self):
        return self.title