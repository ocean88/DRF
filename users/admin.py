from django.contrib import admin

from users.models import User


@admin.register(User)
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email")
