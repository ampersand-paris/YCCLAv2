# Generated by Django 4.0.4 on 2022-05-14 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testkitchenpost',
            options={'ordering': ['-date']},
        ),
    ]
