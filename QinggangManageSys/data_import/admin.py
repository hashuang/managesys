from django.contrib import admin
from . import models

class TransRelationAdmin(admin.ModelAdmin):
    list_display = ('real_meaning', 'own_col', 'from_col')
    search_fields = ('real_meaning', 'own_col','from_col')
    list_filter = ('from_col',)

# Register your models here.
admin.site.register(models.TransRelation,TransRelationAdmin)