# Generated by Django 3.2.8 on 2021-10-23 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ABC_INVENTORY', '0005_alter_user_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='isActive',
            new_name='is_active',
        ),
    ]
