from django.urls import path
from . import views

urlpatterns = [
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('home/', views.homePage, name="home"),
    path('add/', views.addPage, name="add"),
    path('update/', views.updatePage, name="update"),
    path('search/', views.searchPage, name="search"),
    path('deactivate/', views.deactivatePage, name="deactivate"),
    path('reactivate/', views.reactivatePage, name="reactivate"),
    path('report/', views.reportPage, name="report"),


]