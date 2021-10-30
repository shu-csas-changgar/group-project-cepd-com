from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import Group
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
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('firstName')
            messages.success(request, 'Account was created for ' + name)
            return redirect('login')
    return render(request, 'register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


def homePage(request):
    date = datetime.date.today()
    user = request.user
    #Replace nav1 and nav2 with your navigation
    #Make sure to set the width of your entire navigation to be 15%
    #Like width: 15%, that will ensure it's compatible with the home page size
    navigationPage = 'nav2.html'
    if user.is_admin:
        navigationPage = 'nav1.html'
    #Replace Equipments with content from database in exact format
    #i.e a list of dictionaries
    equipments = [
        {'name':"Desktop",
        'active':0,
        'deactivated':0,
        'total':0,},
        {'name':"Laptops",
        'active':0,
        'deactivated':0,
        'total':0,},
        {'name':"Servers",
        'active':0,
        'deactivated':0,
        'total':0,},
        {'name':"Mobile Devices",
        'active':0,
        'deactivated':0,
        'total':0,},
        {'name':"Printers",
        'active':0,
        'deactivated':0,
        'total':0,}
    ]

    context = {
        'date':date,
        'equipments':equipments,
        'user':user,
        'navigationPage':navigationPage,
    }
    return render(request, 'home.html', context)


def updatePage(request):
    return render(request, 'update.html', {})


def deactivatePage(request):
    return render(request, 'deactivate.html', {})

def reactivatePage(request):
    return render(request, 'reactivate.html', {})


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
