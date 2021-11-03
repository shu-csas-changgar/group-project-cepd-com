from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomAccountManager(BaseUserManager):    
    def create_superuser(self, email, firstName, lastName, password, **other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_admin',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_active') is not True:
            raise ValueError(
                'Superuser must be assigned to is_active=True')
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True')

        return self.create_user(email, firstName, lastName, password, **other_fields)

    def create_user(self, email, firstName, lastName, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, firstName = firstName, lastName = lastName,
                            **other_fields)
        user.set_password(password)
        user.save()
        return user    

class Location(models.Model):
    name = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(gettext_lazy('email address'),unique=False)
    phone = models.CharField(max_length=25, null=True)  
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(max_length=150, null=True)
    lastName = models.CharField(max_length=150, null=True)
    email = models.EmailField(gettext_lazy('email address'),unique=True)
    phone = models.CharField(max_length=25, null=True)
    address = models.CharField(max_length=150, null=True)
    officeLocation = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName','lastName'] 

    def __str__(self):
        return str(self.firstName)+' '+str(self.lastName)

class Equipment(models.Model):
    TYPES = (
			('Laptop', 'Laptop'),
			('Desktop', 'Desktop'),
            ('Server', 'Server'),
			('Printer', 'Printer'),
            ('Mobile Device', 'Mobile Device')
			) 

    name = models.CharField(max_length=150, null=True)
    assignedTo = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    officeLocation = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.CASCADE)
    equipmentType = models.CharField(max_length=200, null=True, choices=TYPES)
    purchaseDate = models.DateField(null=True)   
    expirationDate = models.DateField(null=True)
    floor = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.name
