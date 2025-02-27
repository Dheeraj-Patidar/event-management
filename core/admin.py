from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "role")

    def get_readonly_fields(self, request, obj=None):
        return ["password"]


admin.site.register(User, UserAdmin)
