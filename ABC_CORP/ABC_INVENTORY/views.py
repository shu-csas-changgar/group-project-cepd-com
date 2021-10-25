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

    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)



        #firstN = request.POST.get('first-name')
        #lastN = request.POST.get('last-name')
        #email = request.POST.get('email')
        #phone = request.POST.get('phone')
        #password1 = request.POST.get('password1')
        #password2 = request.POST.get('password2')
        #address = request.POST.get('address')
        #location=request.POST.get('location')
        #office=Location(name=location)
        #office.save()

        #user = User.objects.create_user(firstName=firstN, lastName=lastN,
        #                        email=email, phone=phone, address=address,
        #                        officeLocation=office,
        #                        password=password1)

        #form = CreateUserForm(request.POST)
        #print("YEs")
        #print("Yes")
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('firstName')
            messages.success(request, 'Account was created for ' + firstName + " " + lastName)
            return redirect('login')



    return render(request, 'register.html', {'form':form})

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
