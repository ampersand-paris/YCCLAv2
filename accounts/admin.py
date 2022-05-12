from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'time_as_tester', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'time_as_tester', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, AccountAdmin)