from django.contrib import admin

# Register your models here.
from .models import Overview

@admin.register(Overview)
class OverviewAdmin(admin.ModelAdmin):
    pass