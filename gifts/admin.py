from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ["id","first_name", "last_name", "amount", "status", "message" ]

