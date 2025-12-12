from django.contrib import admin
from .models import ShippingAddress
# Register your models here.


@admin.register(ShippingAddress)
class ShippingAdmin(admin.ModelAdmin):
    list_filter = ["created_at" , "updated_at"]