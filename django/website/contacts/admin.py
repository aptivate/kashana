from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import AdminUserChangeForm, AdminUserCreationForm


class UserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('business_email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('business_email', 'password1', 'password2')
        }),
    )
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ('business_email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('business_email', 'first_name', 'last_name')
    ordering = ('business_email',)


admin.site.register(User, UserAdmin)
