from django.contrib import admin
from.models import *

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
      list_display = ['status', 'user','title',
            'description','image','location', 'is_approved']
      list_filter = ['is_approved']
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
 list_display = ['item','user', 'is_approved']  
 list_filter = ['is_approved']