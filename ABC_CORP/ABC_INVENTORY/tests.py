from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Equipment, Location, Vendor

class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com','firstname','lastname','password'
        )
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.firstName, 'firstname')
        self.assertEqual(super_user.lastName, 'lastname')
        self.assertEqual(super_user.is_superuser,True)
        self.assertEqual(super_user.is_staff,True)
        self.assertEqual(super_user.is_active,True)
        self.assertEqual(super_user.is_admin,True)
        self.assertEqual(str(super_user), 'firstname'+' '+'lastname')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            'testuser@super.com','firstname','lastname','password',
            is_superuser=False
        )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email='testuser@super.com',firstName='firstname',lastName='lastname',password='password',
            is_staff=False
        )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com','firstname','lastname','password'
        )
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.firstName, 'firstname')
        self.assertEqual(user.lastName, 'lastname')
        self.assertEqual(user.is_superuser,False)
        self.assertEqual(user.is_staff,True)
        self.assertEqual(user.is_active,True)
        self.assertEqual(user.is_admin,False)
        self.assertEqual(str(user), 'firstname'+' '+'lastname')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email ='',firstName='firstname',lastName='lastname',password='password',
            is_superuser=False
        )

    def test_new_location(self):
        location1 = Location.objects.create(name="TestLocation", is_active=True)
        self.assertEqual(location1.name, "TestLocation")
        self.assertEqual(location1.is_active, True)

        location2 = Location.objects.create(name="TestLocation2", is_active=True)
        self.assertEqual(location2.name, "TestLocation2")
        self.assertEqual(location2.is_active, True)

        location3 = Location.objects.create(name="TestLocation3", is_active=True)
        self.assertEqual(location3.name, "TestLocation3")
        self.assertEqual(location3.is_active, True)

        #Add more more location tests like location2, location3...

    def test_new_vendor(self):
        #create a new vendor like in location
        #and test all vendor properties
        vendor1 = Vendor.objects.create(name="TestLocation", address="TestLocation", email="TestLocation", phone="TestLocation", is_active=True)
        self.assertEqual(vendor1.name, "TestLocation")
        self.assertEqual(vendor1.address, "TestLocation")
        self.assertEqual(vendor1.email, "TestLocation")
        self.assertEqual(vendor1.phone, "TestLocation")
        self.assertEqual(vendor1.is_active, True)

        vendor2 = Vendor.objects.create(name="TestLocation2", address="TestLocation2", email="TestLocation2",
                                        phone="TestLocation2", is_active=True)
        self.assertEqual(vendor2.name, "TestLocation2")
        self.assertEqual(vendor2.address, "TestLocation2")
        self.assertEqual(vendor2.email, "TestLocation2")
        self.assertEqual(vendor2.phone, "TestLocation2")
        self.assertEqual(vendor2.is_active, True)

        vendor3 = Vendor.objects.create(name="TestLocation3", address="TestLocation3", email="TestLocation3",
                                        phone="TestLocation3", is_active=True)
        self.assertEqual(vendor3.name, "TestLocation3")
        self.assertEqual(vendor3.address, "TestLocation3")
        self.assertEqual(vendor3.email, "TestLocation3")
        self.assertEqual(vendor3.phone, "TestLocation3")
        self.assertEqual(vendor3.is_active, True)

    def test_new_equipment(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'firstname', 'lastname', 'password')
        location1 = Location.objects.create(name="TestLocation", is_active=True)
        vendor1 = Vendor.objects.create(name="TestLocation", address="TestLocation", email="TestLocation",
                                        phone="TestLocation", is_active=True)

        equipment1 = Equipment.objects.create( name = "Lenovo Computer", assignedTo = user, officeLocation = location1, vendor = vendor1, equipmentType = "Laptop", purchaseDate = "2007-08-08", expirationDate = "2015-10-06", floor = "5", is_active = True)
        self.assertEqual(equipment1.name, "Lenovo Computer")
        self.assertEqual(equipment1.assignedTo, user)
        self.assertEqual(equipment1.officeLocation, location1)
        self.assertEqual(equipment1.vendor, vendor1)
        self.assertEqual(equipment1.equipmentType, "Laptop")
        self.assertEqual(equipment1.purchaseDate, "2007-08-08")
        self.assertEqual(equipment1.expirationDate, "2015-10-06")
        self.assertEqual(equipment1.floor, "5")
        self.assertEqual(equipment1.is_active, True)




