from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .models import  User, Location, Equipment, Vendor
import datetime


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email OR Password is incorrect')
    return render(request, 'login.html', {})


def registerPage(request):
    locations = Location.objects.all()
    form = CreateUserForm()

    if request.method == 'POST':
        firstName=request.POST.get('first-name')
        lastName=request.POST.get('last-name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        p1=request.POST.get('password1')
        loc=request.POST.get('location')
        location = Location.objects.get(name=loc)
        User.objects.create_user(email=email, firstName=firstName, lastName=lastName, password=p1, phone=phone, address=address, officeLocation=Location(id=location.id))
        messages.success(request, 'Account was created for ' + firstName + " " + lastName)
        return redirect('login')
    return render(request, 'register.html', {'form':form, 'locations':locations})

def logoutUser(request):
    logout(request)
    return redirect('login')

def homePage(request):
    date = datetime.date.today()
    user = request.user
    navigationPage = 'usernav.html'
    if user.is_admin:
        navigationPage = 'adminnav.html'
    #Desktop
    activeDesktop = Equipment.objects.filter(equipmentType="Desktop", is_active=1).count()
    nonActiveDesktop = Equipment.objects.filter(equipmentType="Desktop", is_active=0).count()
    totalDesktop = activeDesktop+nonActiveDesktop

    #Laptop
    activeLaptop = Equipment.objects.filter(equipmentType="Laptop", is_active=1).count()
    nonActiveLaptop = Equipment.objects.filter(equipmentType="Laptop", is_active=0).count()
    totalLaptop = activeLaptop+nonActiveLaptop

    #Server
    activeServer = Equipment.objects.filter(equipmentType="Server", is_active=1).count()
    nonActiveServer = Equipment.objects.filter(equipmentType="Server", is_active=0).count()
    totalServer = activeServer+nonActiveServer

    #Mobile Devices
    activeMD = Equipment.objects.filter(equipmentType="Mobile Device", is_active=1).count()
    nonActiveMD = Equipment.objects.filter(equipmentType="Mobile Device", is_active=0).count()
    totalMD = activeMD+nonActiveMD

    #Printers
    activePrinters = Equipment.objects.filter(equipmentType="Printer", is_active=1).count()
    nonActivePrinters = Equipment.objects.filter(equipmentType="Printer", is_active=0).count()
    totalPrinters = activePrinters+nonActivePrinters

    equipments = [
        {'name':"Desktop",
        'active':activeDesktop,
        'deactivated':nonActiveDesktop,
        'total':totalDesktop,},

        {'name':"Laptops",
        'active':activeLaptop,
        'deactivated':nonActiveLaptop,
        'total':totalLaptop,},

        {'name':"Servers",
        'active':activeServer,
        'deactivated':nonActiveServer,
        'total':totalServer,},

        {'name':"Mobile Devices",
        'active':activeMD,
        'deactivated':nonActiveMD,
        'total':totalMD,},

        {'name':"Printers",
        'active':activePrinters,
        'deactivated':nonActivePrinters,
        'total':totalPrinters,}
    ]

    context = {
        'date':date,
        'equipments':equipments,
        'user':user,
        'navigationPage':navigationPage,
    }
    return render(request, 'home.html', context)

def updateEquipment(request,equipmentId):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
    locations = Location.objects.all()
    users = User.objects.all()
    vendors = Vendor.objects.all()
    e = Equipment.objects.get(id=equipmentId)
    types = ["Laptop", "Desktop", "Server", "Printer", "Mobile Devices"]
    context = {
        'date':date,
        'navigationPage': navigationPage,
        'locations': locations,
        'users': users,
        'vendors': vendors,
        'equipment':e,
        'purchaseDate':str(e.purchaseDate),
        'expirationDate':str(e.expirationDate),
        'equipmentTypes':types,
        'hasAdded':False,
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        assignedToId = int(request.POST.get('assigned_to'))
        officeLocationId = int(request.POST.get('office_location'))
        vendorId = int(request.POST.get('vendor'))
        equipmentType = request.POST.get('equipment_type')
        pd = request.POST.get('purchase_date')
        purchaseDate = datetime.datetime.strptime(pd, '%Y-%m-%d')
        ed = request.POST.get('expiration_date')
        expirationDate = datetime.datetime.strptime(ed, '%Y-%m-%d')
        floor = request.POST.get('floor')

        e.name = name
        e.assignedTo = User(id=assignedToId)
        e.officeLocation = Location(id=officeLocationId)
        e.vendor = Vendor(id=vendorId)
        e.equipmentType = equipmentType
        e.purchaseDate = purchaseDate
        e.expirationDate = expirationDate
        e.floor = floor
        e.is_active = True
        e.save()

        context['hasAdded'] = True
        assignedTo = User.objects.get(id=assignedToId)
        context['assignedTo'] = assignedTo.firstName+' '+assignedTo.lastName
        return render(request, 'updateEquipment.html', context)
    return render(request, 'updateEquipment.html', context)

def updateVendor(request,vendorId):
    v = Vendor.objects.get(id=vendorId)
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'

    context = {
        'date':date,
        'navigationPage': navigationPage,
        'hasAdded':False,
        'vendor':v
    }
    if request.method == 'POST':
        name = request.POST.get('name')        
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        v.name=name
        v.address=address
        v.email=email
        v.phone = phone
        v.save()

        context['hasAdded'] = True
        return render(request, 'updateVendor.html', context)
    return render(request, 'updateVendor.html', context)

def updateUser(request,userId):
    u = User.objects.get(id=userId)
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
    locations = Location.objects.all()
    context = {
        'date':date,
        'navigationPage': navigationPage,
        'locations': locations,
        'user': u,
        'hasAdded':False,        
    }

    if request.method == 'POST':
        firstName=request.POST.get('first_name')
        lastName=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        p1=request.POST.get('password1')
        locId=request.POST.get('location')
        location = Location.objects.get(id=locId)
        is_admin = False if request.POST.get('is_admin') == None else True

        u.email=email
        u.firstName=firstName
        u.lastName=lastName
        u.set_password(p1)
        u.phone=phone
        u.address=address
        u.officeLocation=Location(id=location.id)
        u.is_admin=is_admin
        u.save()

        context['hasAdded'] = True
        officeLocation = Location.objects.get(id=locId)
        context['officeLocation'] = officeLocation
        return render(request, 'updateUser.html', context)
    return render(request, 'updateUser.html', context)

def deactivateEquipment(request,equipmentId):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        e = Equipment.objects.get(id=equipmentId)
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'equipment':e,
        }
        if "yes" in request.POST:
            e.is_active = False
            e.save()
            return redirect('searchEquipment')
        if "no" in request.POST:
            return redirect('searchEquipment')            
        return render(request, 'deactivateEquipment.html', context)
    else:
        return redirect('home')

def deactivateVendor(request,vendorId):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        v = Vendor.objects.get(id=vendorId)
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'vendor':v,
        }

        return render(request, 'deactivateVendor.html', context)
    else:
        return redirect('home')

def deactivateUser(request,userId):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        u = User.objects.get(id=userId)
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'user':u,
        }

        return render(request, 'deactivateUser.html', context)
    else:
        return redirect('home')
    
def displayEquipment(request, equipmentId):
    e = Equipment.objects.get(id=equipmentId)
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'

    context = {'equipment':e, 'navigationPage' : navigationPage, 'date': date}
    return render(request, 'displayEquipment.html', context)

def displayVendor(request, vendorId):
    v = Vendor.objects.get(id=vendorId)
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'

    context = {'vendor':v, 'navigationPage' : navigationPage, 'date': date}
    return render(request, 'displayVendor.html', context)

def displayUser(request, userId):
    u = User.objects.get(id=userId)
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'

    context = {'user':u, 'navigationPage' : navigationPage, 'date': date}
    return render(request, 'displayUser.html', context)

def searchEquipment(request):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'

    users = User.objects.all()
    locations = Location.objects.all()
    vendors = Vendor.objects.all()
    types = ["Laptop", "Desktop", "Server", "Printer", "Mobile Devices"]
    context = {
        'date':date,
        'navigationPage': navigationPage,
        'equipmentTypes': types,
        'users':users,
        'locations': locations,
        'vendors':vendors,
        'hasAdded':False,
    }

    if request.method == 'POST':
        assignedToId = int(request.POST.get('assigned_to'))
        officeLocationId = int(request.POST.get('office_location'))
        vendorId = int(request.POST.get('vendor'))
        equipmentType = request.POST.get('equipment_type')

        selectedassingedTo = "Any"
        selectedofficeLocation = "Any"
        selectedvendor = "Any"
        selectedequipmentType = "Any"

        #Only pulls active Equipments
        equipments = Equipment.objects.filter(is_active=True)
        if assignedToId != -1:
            u = User.objects.get(id=assignedToId)
            selectedassingedTo = u.firstName+" "+u.lastName
            equipments = equipments.filter(assignedTo = u)
        if officeLocationId != -1:
            l = Location.objects.get(id=officeLocationId)
            selectedofficeLocation = str(l.name)
            equipments = equipments.filter(officeLocation = l)
        if vendorId != -1:
            v = Vendor.objects.get(id=vendorId)
            selectedvendor = str(v.name)
            equipments = equipments.filter(vendor = v)
        if equipmentType != "-1":
            selectedequipmentType = equipmentType
            equipments = equipments.filter(equipmentType = equipmentType)

        e = []
        for equipment in equipments:
            asTo = equipment.assignedTo
            e.append(
                {
                    'equipment': equipment,
                    'assignedTo': str(asTo.firstName+' '+asTo.lastName),
                }
            )
        context['selectedassingedTo'] = selectedassingedTo
        context['selectedofficeLocation'] = selectedofficeLocation
        context['selectedvendor'] = selectedvendor
        context['selectedequipmentType'] = selectedequipmentType
        context['hasAdded'] = True
        context['equipments'] = e
        return render(request, 'searchEquipment.html', context)
    return render(request, 'searchEquipment.html', context)

def searchUser(request):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
    context = {
        'date':date,
        'navigationPage': navigationPage,
    }
    
    return render(request, 'searchUser.html', context)

def searchVendor(request):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
    context = {
        'date':date,
        'navigationPage': navigationPage,
    }
    
    return render(request, 'searchVendor.html', context)

def addEquipment(request):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        locations = Location.objects.all()
        users = User.objects.all()
        vendors = Vendor.objects.all()

        context = {
            'date':date,
            'navigationPage': navigationPage,
            'locations': locations,
            'users': users,
            'vendors': vendors,
            'hasAdded':False,
        }

        if request.method == 'POST':
            name = request.POST.get('name')
            assignedToId = int(request.POST.get('assigned_to'))
            officeLocationId = int(request.POST.get('office_location'))
            vendorId = int(request.POST.get('vendor'))
            equipmentType = request.POST.get('equipment_type')
            pd = request.POST.get('purchase_date')
            purchaseDate = datetime.datetime.strptime(pd, '%Y-%m-%d')
            ed = request.POST.get('expiration_date')
            expirationDate = datetime.datetime.strptime(ed, '%Y-%m-%d')
            floor = request.POST.get('floor')

            e = Equipment(name=name,assignedTo=User(id=assignedToId),
                officeLocation=Location(id=officeLocationId),
                vendor=Vendor(id=vendorId), equipmentType=equipmentType,
                purchaseDate=purchaseDate,expirationDate=expirationDate,floor=floor,is_active=True)
            e.save()
            context['hasAdded'] = True
            context['addedEquipment'] = e
            assignedTo = User.objects.get(id=assignedToId)
            context['assignedTo'] = assignedTo.firstName+' '+assignedTo.lastName
            return render(request, 'addEquipment.html', context)
        return render(request, 'addEquipment.html', context)
    else:
        return redirect('home')

def addVendor(request):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'hasAdded':False,
        }
        if request.method == 'POST':
            name = request.POST.get('name')        
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            v = Vendor(name=name,address=address,
                email=email, phone = phone)
            v.save()
            context['hasAdded'] = True
            context['addedVendor'] = v
            return render(request, 'addVendor.html', context)
        return render(request, 'addVendor.html', context)
    else:
        return redirect('home')

def addUser(request):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        locations = Location.objects.all()

        context = {
            'date':date,
            'navigationPage': navigationPage,
            'locations': locations,
            'hasAdded':False,
        }

        if request.method == 'POST':
            firstName=request.POST.get('first_name')
            lastName=request.POST.get('last_name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            p1=request.POST.get('password1')
            locId=request.POST.get('location')
            location = Location.objects.get(id=locId)
            is_admin = False if request.POST.get('is_admin') == None else True

            u = User.objects.create_user(email=email, firstName=firstName,
            lastName=lastName, password=p1, phone=phone, address=address,
            officeLocation=Location(id=location.id),is_admin=is_admin)

            context['hasAdded'] = True
            context['addedUser'] = u
            officeLocation = Location.objects.get(id=locId)
            context['officeLocation'] = officeLocation
            return render(request, 'addUser.html', context)
        return render(request, 'addUser.html', context)
    else:
        return redirect('home')
    
def reportPage(request):
    date = datetime.date.today()
    user = request.user
    navigationPage = 'usernav.html'
    if user.is_admin:
        navigationPage = 'adminnav.html'   
    context = {
        'date':date,
        'user':user,
        'navigationPage':navigationPage,
    }    
    return render(request, 'report.html', context)

def importPage(request):
    return render(request, 'import.html', {})

def exportPage(request):
    return render(request, 'export.html', {})

def accountPage(request):
    u = request.user
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
    locations = Location.objects.all()
    context = {
        'date':date,
        'navigationPage': navigationPage,
        'locations': locations,
        'user': u, 
    }

    if request.method == 'POST':
        firstName=request.POST.get('first_name')
        lastName=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        p1=request.POST.get('password1')
        locId=request.POST.get('location')
        location = Location.objects.get(id=locId)
        is_admin = False if request.POST.get('is_admin') == None else True

        u.email=email
        u.firstName=firstName
        u.lastName=lastName
        u.set_password(p1)
        u.phone=phone
        u.address=address
        u.officeLocation=Location(id=location.id)
        u.is_admin=is_admin
        u.save()
        return redirect('logout')
    return render(request, 'account.html', context)

