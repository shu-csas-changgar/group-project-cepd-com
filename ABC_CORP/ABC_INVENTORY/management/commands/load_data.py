from ...models import Location, Vendor, Equipment, User
from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from pytz import UTC
from django.contrib.auth import get_user_model

DATE_FORMAT = '%m/%d/%Y'

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from csv files onto our database"

    def handle(self, *args, **options):
        print("Creating Unassinged User")
        db = get_user_model()
        db.objects.create_user('unassinged@gmail.com','Unassigned','','')
        print('Unassinged User Created')

        print("Creating Super User")
        db = get_user_model()
        db.objects.create_superuser('super@gmail.com','Super','Super','password')
        print('Super User Created')

        print("Loading Location data")
        for row in DictReader(open('./location.csv')):
            location = Location()
            location.name = row['name']
            location.is_active = row['is_active']
            location.save()
        print("Location data loaded successfully")
        print("Loading Vendor data")
        for row in DictReader(open('./vendor.csv')):
            vendor = Vendor()
            vendor.name = row['name']
            vendor.address = row['address']
            vendor.email = row['email']
            vendor.phone = row['phone']
            vendor.is_active = row['is_active']
            vendor.save()
        print("Vendor data loaded successfully")
        print("Loading Equipment data")
        for row in DictReader(open('./equipment.csv')):
            equipment = Equipment()
            equipment.name = row['name']
            equipment.equipmentType = row['equipmentType']
            purDate = row['purchaseDate']
            expDate = row['expirationDate']
            cleanedPurDate = UTC.localize(
                datetime.strptime(purDate, DATE_FORMAT))
            cleanedExpDate = UTC.localize(
                datetime.strptime(expDate, DATE_FORMAT))            
            equipment.purchaseDate = cleanedPurDate
            equipment.expirationDate = cleanedExpDate
            equipment.floor = row['floor']
            equipment.is_active = True if row['is_active'] == "1" else False            
            equipment.assignedTo = User.objects.get(id=int(row['assignedTo_id']))
            equipment.officeLocation = Location.objects.get(id=int(row['officeLocation_id']))
            equipment.vendor = Vendor.objects.get(id=int(row['vendor_id']))
            equipment.save()
        print("Equipment data loaded successfully")

