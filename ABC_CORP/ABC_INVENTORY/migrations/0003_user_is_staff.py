# Generated by Django 3.2.8 on 2021-10-23 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABC_INVENTORY', '0002_auto_20211023_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]