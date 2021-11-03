from django.urls import path
from . import views

urlpatterns = [
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('home/', views.homePage, name="home"),
    path('addEquipment/', views.addEquipment, name="addEquipment"),
    path('updateEquipment/<int:equipmentId>', views.updateEquipment, name="updateEquipment"),
    path('search/', views.searchPage, name="search"),
    path('displayEquipment/<int:equipmentId>', views.displayEquipment, name="displayEquipment"),
    path('displayVendor/<int:vendorId>', views.displayEquipment, name="displayVendor"),
    path('displayUser/<int:userId>', views.displayEquipment, name="displayUser"),
    path('deactivateEquipment/<int:equipmentId>', views.deactivateEquipment, name="deactivateEquipment"),
    path('deactivateVendor/<int:vendorId>', views.deactivateVendor, name="deactivateVendor"),
    path('deactivateUser/<int:userId>', views.deactivateUser, name="deactivateUser"),
    path('reactivate/', views.reactivatePage, name="reactivate"),
    path('report/', views.reportPage, name="report"),


]