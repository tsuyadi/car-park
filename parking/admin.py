from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'config_key', 'config_value', 'created', 'modified']
    list_filter = ('config_key',)
    search_fields = ['config_key']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


