from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import Group
from .models import  User, Location

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
    #print(locations.count())
    #locations = ["NYC", "Seattle", "Jersey City"]
    #locs = list(location.name for location in locations)
    form = CreateUserForm()

    if request.method == 'POST':


        firstName=request.POST.get('first-name')
        lastName=request.POST.get('last-name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        p1=request.POST.get('password1')
        p2=request.POST.get('password2')
        loc=request.POST.get('location')

        location = Location.objects.get(name=loc)
        #print(place.id)

        #loc2 = Location(name=loc)
        #loc.save()


        new_user = User.objects.create_user(email=email, firstName=firstName, lastName=lastName, password=p1, phone=phone, address=address, officeLocation=Location(id=location.id))
        messages.success(request, 'Account was created for ' + firstName + " " + lastName)
        return redirect('login')
    return render(request, 'register.html', {'form':form, 'locations':locations})

def logoutUser(request):
    pass

def homePage(request):
    return render(request, 'home.html', {})

def updatePage(request):
    return render(request, 'update.html', {})

def deactivatePage(request):
    return render(request, 'deactivate.html', {})

def displayPage(request):
    return render(request, 'display.html', {})

def searchPage(request):
    return render(request, 'search.html', {})

def addPage(request):
    return render(request, 'add.html', {})

def reportPage(request, isImport):
    if(isImport):
        print('Importing CSV')
    else:
        print('Exporting CSV')
    return render(request, 'report.html', {})

def accountPage(request):
    return render(request, 'account.html', {})
