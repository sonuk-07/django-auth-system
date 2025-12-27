from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Configure how User appears in admin panel
    """
    model = CustomUser

    #what fields to show in user list
    list_display = ['email', 'first_name','last_name', 'is_staff','is_verified']

    #what to search by
    search_fields = ['email', 'first_name', 'last_name']

    #what can be filtered
    list_filter = ['is_staff','is_active','is_verified']

    #how to organize fields in user detail page
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal Info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )

    #fields when adding new user 
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    #use email for ordering
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
