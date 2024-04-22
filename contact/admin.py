from django.contrib import admin
from .models import ContactUs

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "message"]


admin.site.register(ContactUs, ContactAdmin)
