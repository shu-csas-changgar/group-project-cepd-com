# Generated by Django 3.2.8 on 2021-10-23 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=25, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('firstName', models.CharField(max_length=150, null=True)),
                ('lastName', models.CharField(max_length=150, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=25, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('officeLocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ABC_INVENTORY.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('equipmentType', models.CharField(choices=[('Laptop', 'Laptop'), ('Desktop', 'Desktop'), ('Server', 'Server'), ('Printer', 'Printer'), ('Mobile Device', 'Mobile Device')], max_length=200, null=True)),
                ('purchaseDate', models.DateField(null=True)),
                ('expirationDate', models.DateField(null=True)),
                ('floor', models.CharField(max_length=100, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ABC_INVENTORY.user')),
                ('officeLocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ABC_INVENTORY.location')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ABC_INVENTORY.vendor')),
            ],
        ),
    ]