from django.urls import path
from . import views

urlpatterns = [
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('home/', views.homePage, name="home"),
    path('addEquipment/', views.addEquipment, name="addEquipment"),
    path('addVendor/', views.addVendor, name="addVendor"),
    path('addUser/', views.addUser, name="addUser"),
    path('updateEquipment/<int:equipmentId>', views.updateEquipment, name="updateEquipment"),
    path('updateVendor/<int:vendorId>', views.updateVendor, name="updateVendor"),
    path('updateUser/<int:userId>', views.updateUser, name="updateUser"),
    path('search/', views.searchPage, name="search"),
    path('displayEquipment/<int:equipmentId>', views.displayEquipment, name="displayEquipment"),
    path('displayVendor/<int:vendorId>', views.displayVendor, name="displayVendor"),
    path('displayUser/<int:userId>', views.displayUser, name="displayUser"),
    path('deactivateEquipment/<int:equipmentId>', views.deactivateEquipment, name="deactivateEquipment"),
    path('deactivateVendor/<int:vendorId>', views.deactivateVendor, name="deactivateVendor"),
    path('deactivateUser/<int:userId>', views.deactivateUser, name="deactivateUser"),
    path('report/', views.reportPage, name="report"),
    path('account/', views.accountPage, name="account"),


]