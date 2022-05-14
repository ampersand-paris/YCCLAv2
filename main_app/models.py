from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import ImageField

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = ArrayField(models.CharField(max_length=100)) 
    preparation = ArrayField(models.CharField(max_length=1000)) 
    image = models.ImageField(upload_to='./media', default=False)
    background_color = models.CharField(max_length=100, default="var(--main-blue)")
    secondary_color = models.CharField(max_length=100, default="var(--main-red)")

    def __str__(self):
        return self.title