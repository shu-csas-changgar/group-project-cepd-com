from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from Registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
]
