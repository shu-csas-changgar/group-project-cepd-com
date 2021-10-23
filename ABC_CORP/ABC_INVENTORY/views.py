from django.shortcuts import render

def loginPage(request):
    return render(request, 'login.html', {})

def registerPage(request):
    return render(request, 'register.html', {})

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
