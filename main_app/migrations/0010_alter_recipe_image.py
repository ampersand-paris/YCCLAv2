# Generated by Django 4.0.4 on 2022-05-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_recipe_secondary_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=False, upload_to='./static'),
        ),
    ]
