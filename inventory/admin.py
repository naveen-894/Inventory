from django.contrib import admin

from inventory.models import AdminUser, Item

# Register your models here.

admin.site.register(Item)
admin.site.register(AdminUser)