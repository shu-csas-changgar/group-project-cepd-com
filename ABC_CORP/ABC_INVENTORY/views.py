from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import  User, Location, Equipment, Vendor
from django.contrib import messages
from .forms import CreateUserForm
from django.http import HttpResponse
from .forms import UploadFileForm
from csv import DictReader
from datetime import datetime as dt
import datetime
from pytz import UTC
import csv
import os
import re

def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or emailValidator(email) != True:
            errorMessage = "Invalid Email Submitted, kindly try again"
            redirectUrlName = "login"
            redirectPageName= "Login"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if not password:
            errorMessage = "Password is empty"
            redirectUrlName = "login"
            redirectPageName= "Login"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        userExist = User.objects.filter(email = email).exists()

        if(not userExist):
            messages.info(request, 'User does not Exist')
            return render(request, 'login.html', {})

        u = User.objects.get(email = email)
        if(u != None and not u.is_active):
            messages.info(request, 'Contact Admin to Activate User')
            return render(request, 'login.html', {})

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
        p2=request.POST.get('password2')
        loc=int(request.POST.get('location'))
        location = Location.objects.get(id=loc)

        if emailValidator(email) != True:
            errorMessage = "Invalid Email Submitted, kindly try again"
            redirectUrlName = "register"
            redirectPageName= "Register"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if phoneValidator(phone) != True:
            errorMessage = "Invalid Phone Submitted, kindly try again"
            redirectUrlName = "register"
            redirectPageName= "Register"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        userExists=User.objects.filter(email=email).exists()

        if userExists:
            errorMessage = "A user with the email you entered currently exists in the system, Kindly try again."
            redirectUrlName = "register"
            redirectPageName= "Register"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if p1 != p2:
            errorMessage = "Passwords do not match, enter the same password for both password fields."
            redirectUrlName = "register"
            redirectPageName= "Register"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        user = User.objects.create_user(email=email, firstName=firstName, lastName=lastName, password=p1, phone=phone, address=address, officeLocation=Location(id=location.id))
        user.is_active = False
        user.save()
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

        if expirationDate < purchaseDate:
            errorMessage = "Expiration date is earlier than Purchase date, ensure Purchase date is earlier than Expiration date."
            redirectUrlName = "addEquipment"
            redirectPageName= "Add Equipment"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)


        e.name = name
        e.assignedTo = User(id=assignedToId)
        e.officeLocation = Location(id=officeLocationId)
        e.vendor = Vendor(id=vendorId)
        e.equipmentType = equipmentType
        e.purchaseDate = purchaseDate
        e.expirationDate = expirationDate
        e.floor = floor
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


        if emailValidator(email) != True:
            errorMessage = "Invalid Email Submitted, kindly try again"
            redirectUrlName = "updateVendor"
            redirectPageName= "Update Vendor"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName,vendorId)


        if phoneValidator(phone)!=True:
            errorMessage = "Invalid Phone Submitted, kindly try again"
            redirectUrlName = "updateVendor"
            redirectPageName= "Update Vendor"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, vendorId)

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
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        locations = Location.objects.all()
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'locations': locations,
            'user': u,
            'loggedOnUser': request.user,
            'hasAdded':False,
        }

        if request.method == 'POST':
            firstName=request.POST.get('first_name')
            lastName=request.POST.get('last_name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            p1=request.POST.get('password1')
            p2=request.POST.get('password2')
            locId=request.POST.get('location')
            location = Location.objects.get(id=locId)
            is_admin = False
            if(u.is_admin):
                is_admin = False if request.POST.get('is_admin') == None else True

            if emailValidator(email) != True:
                errorMessage = "Invalid Email Submitted, kindly try again"
                redirectUrlName = "updateUser"
                redirectPageName= "Update User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)

            if phoneValidator(phone)!=True:
                errorMessage = "Invalid Phone Submitted, kindly try again"
                redirectUrlName = "updateUser"
                redirectPageName= "Update User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)

            userExists=User.objects.filter(email=email).exists()

            if userExists and email != u.email:
                errorMessage = "A user with the email you entered currently exists in the system, Kindly try again."
                redirectUrlName = "updateUser"
                redirectPageName= "Update User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)

            if p1 != p2:
                errorMessage = "Passwords do not match, enter the same password for both password fields."
                redirectUrlName = "updateUser"
                redirectPageName= "Update User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)

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

            if email == request.user.email:
                return redirect('logout')
            return render(request, 'updateUser.html', context)
        return render(request, 'updateUser.html', context)
    else:
        errorMessage = "Non Admins cannot Update Users."
        redirectUrlName = "searchUser"
        redirectPageName= "Search User"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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
        errorMessage = "Non Admins cannot Deactivate Equipment."
        redirectUrlName = "searchEquipment"
        redirectPageName= "Search Equipment"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)


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
        if "yes" in request.POST:
            v.is_active = False
            v.save()
            return redirect('searchVendor')
        if "no" in request.POST:
            return redirect('searchVendor')
        return render(request, 'deactivateVendor.html', context)
    else:
        errorMessage = "Non Admins cannot Deactivate Vendor."
        redirectUrlName = "searchVendor"
        redirectPageName= "Search Vendor"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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
        if request.user.id == userId:
            errorMessage = "Bad Operation, User you are attempting to deactivate is currently logged in."
            redirectUrlName = "searchUser"
            redirectPageName = "Search User"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)
        
        elif "Yes" in request.POST:
            u.is_active = False
            u.save()
            return redirect('searchUser')
        elif "No" in request.POST:
            return redirect('searchUser')
        else:
            return render(request, 'deactivateUser.html', context)
    else:
        errorMessage = "Non Admins cannot Deactivate User."
        redirectUrlName = "searchUser"
        redirectPageName= "Search User"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

def activateEquipment(request,equipmentId):
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
            e.is_active = True
            e.save()
            return redirect('searchEquipment')
        if "no" in request.POST:
            return redirect('searchEquipment')
        return render(request, 'activateEquipment.html', context)
    else:
        errorMessage = "Non Admins cannot Activate Equipment."
        redirectUrlName = "searchEquipment"
        redirectPageName= "Search Equipment"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, equipmentId)


def activateVendor(request,vendorId):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        v = Vendor.objects.get(id=vendorId)
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'vendor':v,
        }
        if "yes" in request.POST:
            v.is_active = True
            v.save()
            return redirect('searchVendor')
        if "no" in request.POST:
            return redirect('searchVendor')
        return render(request, 'activateVendor.html', context)
    else:
        errorMessage = "Non Admins cannot Activate Vendor."
        redirectUrlName = "searchVendor"
        redirectPageName= "Search Vendor"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, vendorId)

def activateUser(request,userId):
    date = datetime.date.today()
    navigationPage = 'adminnav.html'
    if request.user.is_admin:
        u = User.objects.get(id=userId)
        context = {
            'date':date,
            'navigationPage': navigationPage,
            'user':u,
        }
        if "Yes" in request.POST:
            u.is_active = True
            u.save()
            return redirect('searchUser')
        elif "No" in request.POST:
            return redirect('searchUser')
        else:
            return render(request, 'activateUser.html', context)
    else:
        errorMessage = "Non Admins cannot Activate User."
        redirectUrlName = "searchUser"
        redirectPageName= "Search User"
        return errorHandler(request, errorMessage, redirectUrlName, redirectPageName, userId)

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
    isAdmin = False
    is_inactive = False
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
        isAdmin = True

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
        'isAdmin': isAdmin
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        assignedToId = int(request.POST.get('assigned_to'))
        officeLocationId = int(request.POST.get('office_location'))
        vendorId = int(request.POST.get('vendor'))
        equipmentType = request.POST.get('equipment_type')
        if isAdmin:
            is_inactive= False if request.POST.get('is_inactive') == None else True

        selectedName = "Any"
        selectedassingedTo = "Any"
        selectedofficeLocation = "Any"
        selectedvendor = "Any"
        selectedequipmentType = "Any"
        selectedIsInactive = "False"

        equipments = Equipment.objects.all()
        if name != "":
            selectedName = name
            equipments = equipments.filter(name = name)
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
        selectedIsInactive = is_inactive
        if is_inactive == True:
            equipments = equipments.filter(is_active=False)
        if is_inactive == False:
            equipments = equipments.filter(is_active=True)

        e = []
        for equipment in equipments:
            asTo = equipment.assignedTo
            e.append(
                {
                    'equipment': equipment,
                    'assignedTo': str(asTo.firstName+' '+asTo.lastName),
                }
            )

        context['selectedName'] = selectedName
        context['selectedassingedTo'] = selectedassingedTo
        context['selectedofficeLocation'] = selectedofficeLocation
        context['selectedvendor'] = selectedvendor
        context['selectedequipmentType'] = selectedequipmentType
        context['selectedIsInactive'] = selectedIsInactive
        context['totalQueryCount'] = equipments.count()
        unassingedUser = User.objects.get(id=1)
        context['totalAssignedCount'] = equipments.exclude(assignedTo = unassingedUser).count()
        context['totalUnassignedCount'] = equipments.filter(assignedTo = unassingedUser).count()
        context['hasAdded'] = True
        context['equipments'] = e
        return render(request, 'searchEquipment.html', context)
    return render(request, 'searchEquipment.html', context)

def searchUser(request):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    locations = Location.objects.all()
    isAdmin = False
    is_inactive = False
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
        isAdmin = True

    context = {
            'date':date,
            'navigationPage': navigationPage,
            'locations':locations,
            'hasAdded':False,
            'isAdmin': isAdmin
    }
    if request.method == 'POST':
        firstName=request.POST.get('first-name')
        lastName=request.POST.get('last-name')
        email=request.POST.get('email')
        locationId=int(request.POST.get('location'))
        is_admin= False if request.POST.get('is_admin') == None else True
        if isAdmin:
            is_inactive= False if request.POST.get('is_inactive') == None else True


        if email != "" and emailValidator(email) != True:
            if emailValidator(email) != True:
                errorMessage = "Invalid Email Submitted, kindly try again"
                redirectUrlName = "searchUser"
                redirectPageName= "Search User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        selectedFName = "Any"
        selectedLName = "Any"
        selectedEmail = "Any"
        selectedLocation = "Any"
        selectedIsAdmin = "Any"
        selectedIsInactive = "False"

        users = User.objects.all().exclude(id=1)
        if firstName != "":
            selectedFName = firstName
            users=users.filter(firstName=firstName)
        if lastName != "":
            selectedLName=lastName
            users=users.filter(lastName=lastName)
        if email != "":
            selectedEmail = email
            users=users.filter(email=email)
        if locationId != -1:
            locationOBJ = Location.objects.get(id=locationId)
            selectedLocation = locationOBJ.name
            users = users.filter(officeLocation=locationOBJ)
        selectedIsAdmin = is_admin
        if is_admin == True:
            users = users.filter(is_admin=True)
        if is_admin == False:
            users = users.filter(is_admin=False)
        selectedIsInactive = is_inactive
        if is_inactive == True:
            users = users.filter(is_active=False)
        if is_inactive == False:
            users = users.filter(is_active=True)

        context['users'] = users
        context['selectedFName'] = selectedFName
        context['selectedLName'] = selectedLName
        context['selectedEmail'] = selectedEmail
        context['selectedLocation'] = selectedLocation
        context['selectedIsAdmin'] = selectedIsAdmin
        context['selectedIsInactive'] = selectedIsInactive
        context['totalQueryCount'] = users.count()
        context['hasAdded'] = True
        return render(request, 'searchUser.html', context)
    return render(request, 'searchUser.html', context)

def searchVendor(request):
    date = datetime.date.today()
    navigationPage = 'usernav.html'
    isAdmin = False
    is_inactive = False
    if request.user.is_admin:
        navigationPage = 'adminnav.html'
        isAdmin = True

    context = {
        'date':date,
        'navigationPage': navigationPage,
        'hasAdded':False,
        'isAdmin' : isAdmin,
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if isAdmin:
            is_inactive= False if request.POST.get('is_inactive') == None else True

        if phone != "" and phoneValidator(phone)!=True:
            errorMessage = "Invalid Phone Submitted, kindly try again"
            redirectUrlName = "searchVendor"
            redirectPageName= "Search Vendor"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if email != "" and emailValidator(email) != True:
            errorMessage = "Invalid Email Submitted, kindly try again"
            redirectUrlName = "searchVendor"
            redirectPageName= "Search Vendor"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        selectedName = "Any"
        selectedAddress = "Any"
        selectedEmail = "Any"
        selectedPhone = "Any"
        selectedIsInactive = "False"

        vendors = Vendor.objects.all()
        if name != "":
            selectedName = name
            vendors = vendors.filter(name = name)
        if address != "":
            selectedAddress = address
            vendors = vendors.filter(address = address)
        if email != "":
            selectedEmail = email
            vendors = vendors.filter(email = email)
        if phone != "":
            selectedPhone = phone
            vendors = vendors.filter(phone = phone)
        selectedIsInactive = is_inactive
        if is_inactive == True:
            vendors = vendors.filter(is_active=False)
        if is_inactive == False:
            vendors = vendors.filter(is_active=True)

        context['vendors'] = vendors
        context['selectedName'] = selectedName
        context['selectedAddress'] = selectedAddress
        context['selectedEmail'] = selectedEmail
        context['selectedPhone'] = selectedPhone
        context['selectedIsInactive'] = selectedIsInactive
        context['totalQueryCount'] = vendors.count()
        context['hasAdded'] = True
        return render(request, 'searchVendor.html', context)

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

            if expirationDate < purchaseDate:
                errorMessage = "Expiration date is earlier than Purchase date, ensure Purchase date is earlier than Expiration date."
                redirectUrlName = "addEquipment"
                redirectPageName= "Add Equipment"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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

            if emailValidator(email) != True:
                errorMessage = "Invalid Email Submitted, kindly try again"
                redirectUrlName = "addVendor"
                redirectPageName= "Add Vendor"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

            if phoneValidator(phone) != True:
                errorMessage = "Invalid Phone Submitted, kindly try again"
                redirectUrlName = "addVendor"
                redirectPageName= "Add Vendor"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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
            p2=request.POST.get('password2')
            locId=request.POST.get('location')
            location = Location.objects.get(id=locId)
            is_admin = False if request.POST.get('is_admin') == None else True

            if emailValidator(email) != True:
                errorMessage = "Invalid Email Submitted, kindly try again"
                redirectUrlName = "addUser"
                redirectPageName= "Add User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

            if phoneValidator(phone)!=True:
                errorMessage = "Invalid Phone Submitted, kindly try again"
                redirectUrlName = "addUser"
                redirectPageName= "Add User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

            userExists=User.objects.filter(email=email).exists()

            if userExists:
                errorMessage = "A user with the email you entered currently exists in the system, Kindly try again."
                redirectUrlName = "addUser"
                redirectPageName= "Add User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

            if p1 != p2:
                errorMessage = "Passwords do not match, enter the same password for both password fields."
                redirectUrlName = "addUser"
                redirectPageName= "Add User"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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

def importPage(request):
    if(request.user.is_admin):
        date = datetime.date.today()
        navigationPage = 'adminnav.html'

        context = {
            'date':date,
            'navigationPage':navigationPage,
        }

        if "Download Template" in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="equipmentTemplate.csv"'

            writer = csv.writer(response)
            writer.writerow(['name', 'equipmentType', 'purchaseDate', 'expirationDate', 'floor', 'officeLocation_id', 'vendor_id'])
            equipments = Equipment.objects.all().values_list('name', 'equipmentType', 'purchaseDate', 'expirationDate', 'floor', 'officeLocation_id', 'vendor_id')
            
            writer.writerow(equipments.get(id=1))
            return response

        if "Import" in request.POST:
            if not request.FILES:
                errorMessage = "No File Selected, Kindly Select File"
                redirectUrlName = "import"
                redirectPageName= "Import"
                return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)
            
            form = UploadFileForm(request.POST, request.FILES)            
            if form.is_valid():
                handle_uploaded_file(request, request.FILES['file'])
                context['form'] = UploadFileForm()
                return render(request, 'import.html', context)

        form = UploadFileForm()
        context['form'] = form
        return render(request, 'import.html', context)
    else:
        return redirect('home')

def handle_uploaded_file(request,f):
    DATE_FORMAT = '%m/%d/%Y'
    with open('./uploaded.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    for row in DictReader(open('./uploaded.csv')):
        equipment = Equipment()
        equipment.name = row['name']
        equipment.equipmentType = row['equipmentType']
        purDate = row['purchaseDate']
        expDate = row['expirationDate']
        cleanedPurDate = UTC.localize(
            dt.strptime(purDate, DATE_FORMAT))
        cleanedExpDate = UTC.localize(
            dt.strptime(expDate, DATE_FORMAT))
        equipment.purchaseDate = cleanedPurDate
        equipment.expirationDate = cleanedExpDate
        equipment.floor = row['floor']
        equipment.is_active = False
        equipment.assignedTo = User.objects.get(id=1)
        equipment.officeLocation = Location.objects.get(id=int(row['officeLocation_id']))
        equipment.vendor = Vendor.objects.get(id=int(row['vendor_id']))
        equipment.save()
    os.remove("uploaded.csv")
    messages.info(request, 'Equipments Uploaded Succesfully!')

def exportPage(request):
    date = datetime.date.today()
    user = request.user
    navigationPage = 'usernav.html'
    if user.is_admin:
        navigationPage = 'adminnav.html'
    context = {
        'date':date,
        'navigationPage':navigationPage,
    }
    if "Export" in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="equipments.csv"'
        writer = csv.writer(response)

        writer.writerow(['Equipments'])
        writer.writerow(['name', 'equipmentType', 'purchaseDate', 'expirationDate', 'floor', 'is_active', 'assignedToUser_id', 'officeLocation_id', 'vendor_id'])
        equipments = Equipment.objects.all().values_list('name', 'equipmentType', 'purchaseDate', 'expirationDate', 'floor', 'is_active', 'assignedTo_id', 'officeLocation_id', 'vendor_id')
        for equipment in equipments:
            writer.writerow(equipment)
        writer.writerow([''])

        if request.user.is_admin:
            writer.writerow(['Users'])
            writer.writerow(['id','firstName', 'lastName', 'email', 'phone', 'address', 'officeLocation', 'is_active', 'is_admin'])
            users = User.objects.all().exclude(id=1).values_list('id','firstName', 'lastName', 'email', 'phone', 'address', 'officeLocation', 'is_active', 'is_admin')
            for user in users:
                writer.writerow(user)
            writer.writerow([''])

            writer.writerow(['Vendors'])
            writer.writerow(['id','name', 'address', 'email', 'phone', 'is_active'])
            vendors = Vendor.objects.all().values_list('id','name', 'address', 'email', 'phone', 'is_active')
            for vendor in vendors:
                writer.writerow(vendor)
            writer.writerow([''])

            writer.writerow(['Locations'])
            writer.writerow(['id','name', 'is_active'])
            locations = Location.objects.all().values_list('id','name', 'is_active')
            for location in locations:
                writer.writerow(location)
            writer.writerow([''])

        return response
    return render(request, 'export.html', context)

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
        p2=request.POST.get('password2')
        locId=request.POST.get('location')
        location = Location.objects.get(id=locId)
        is_admin = False
        if(u.is_admin):
            is_admin = False if request.POST.get('is_admin') == None else True

        if emailValidator(email) != True:
            errorMessage = "Invalid Email Submitted, kindly try again"
            redirectUrlName = "account"
            redirectPageName= "Account"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if phoneValidator(phone)!=True:
            errorMessage = "Invalid Phone Submitted, kindly try again"
            redirectUrlName = "account"
            redirectPageName= "Account"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        userExists=User.objects.filter(email=email).exists()

        if userExists and email!=request.user.email:
            errorMessage = "A user with the email you entered currently exists in the system, Kindly try again."
            redirectUrlName = "account"
            redirectPageName= "Account"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

        if p1 != p2:
            errorMessage = "Passwords do not match, enter the same password for both password fields."
            redirectUrlName = "account"
            redirectPageName= "Account"
            return errorHandler(request, errorMessage, redirectUrlName, redirectPageName)

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

def errorHandler(request,errorMessage, redirectUrlName, redirectPageName, someParameterValue = -1):
    date = datetime.date.today()
    context = {
            'date':date,
            'errorMessage':errorMessage,
            'redirectUrlName': redirectUrlName,
            'redirectPageName': redirectPageName,
            'someParameterValue' : someParameterValue,
        }
    return render(request, 'error.html', context)

def emailValidator(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False

def phoneValidator(phone):
    regex = "^([\s\d]+)$"
    if re.fullmatch(regex, phone) and len(phone) == 10:
        return True
    else:
        return False
