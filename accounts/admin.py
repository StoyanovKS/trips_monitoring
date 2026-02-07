from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "preferred_currency",
        "timezone",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Preferences", {"fields": ("preferred_currency", "timezone")}),
    )


    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Preferences", {"fields": ("preferred_currency", "timezone")}),
    )
