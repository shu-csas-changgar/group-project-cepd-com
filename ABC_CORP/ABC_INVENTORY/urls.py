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
    path('searchEquipment/', views.searchEquipment, name="searchEquipment"),
    path('searchUser/', views.searchUser, name="searchUser"),
    path('searchVendor/', views.searchVendor, name="searchVendor"),
    path('displayEquipment/<int:equipmentId>', views.displayEquipment, name="displayEquipment"),
    path('displayVendor/<int:vendorId>', views.displayVendor, name="displayVendor"),
    path('displayUser/<int:userId>', views.displayUser, name="displayUser"),
    path('deactivateEquipment/<int:equipmentId>', views.deactivateEquipment, name="deactivateEquipment"),
    path('deactivateVendor/<int:vendorId>', views.deactivateVendor, name="deactivateVendor"),
    path('deactivateUser/<int:userId>', views.deactivateUser, name="deactivateUser"),
    path('import/', views.importPage, name="import"),
    path('export/', views.exportPage, name="export"),
    path('account/', views.accountPage, name="account"),
    path('error/<str:errorMessage>/<str:redirectUrlName>/<str:redirectPageName>', views.errorHandler, name="error"),
    path('error/<str:errorMessage>/<str:redirectUrlName>/<str:redirectPageName>/<int:someParameterValue>', views.errorHandler, name="error"),


]