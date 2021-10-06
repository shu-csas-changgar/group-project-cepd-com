from django.shortcuts import render

# Create your views here.
def index(request):
    data = {
        'name': 'Garett Chang',
        'email': 'changgar@shu.edu',
        'message': 'Hello from CSAS 4117'
    }
    return render(request, 'Index.html', context=data)