from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin interface
    model = User
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'phone', 'gender', 'value', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Define the fields that will appear in the detail view for users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Information', {'fields': ('role', 'value')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define the fields to be shown in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'gender', 'role'),
        }),
    )

    # Add functionality to add and edit custom user
    filter_horizontal = ('groups', 'user_permissions')

# Register the custom User model with the admin
admin.site.register(User, CustomUserAdmin)
