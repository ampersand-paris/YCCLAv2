# Generated by Django 4.0.4 on 2022-05-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='background_color',
            field=models.CharField(default='var(--main-blue)', max_length=100),
        ),
    ]
