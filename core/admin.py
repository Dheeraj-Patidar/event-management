from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")

    list_editable = ("is_active", "is_staff")

    list_filter = ("role", "is_active", "is_staff")

    search_fields = ("email", "first_name", "last_name", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "phone_number", "role")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    ordering = ("email",)
admin.site.register(User, CustomUserAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "date", "location", "created_at", "expired")  # Display expired status

    # def expired(self, obj):
    #     return obj.expired

    # expired.boolean = True  

admin.site.register(Event, EventAdmin)