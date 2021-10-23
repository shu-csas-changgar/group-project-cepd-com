from django.contrib import admin
from .models import User, Equipment, Location, Vendor
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    search_fields = ('email','firstName','lastName')
    ordering = ('email',)
    list_display = ('email','firstName','lastName','is_active','is_staff')    

admin.site.register(User, UserAdminConfig)
admin.site.register(Equipment)
admin.site.register(Location)
admin.site.register(Vendor)
