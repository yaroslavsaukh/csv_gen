from django.contrib import admin
from .models import *


# Register your models here.

class SchemasAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'column_sep', 'string_character')
    list_display_links = ('pk', 'name')


class ColumnsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'data_type')
    list_display_links = ('pk', 'name')


class SetsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'schema')
    list_display_links = ('pk',)


admin.site.register(SchemaModel, SchemasAdmin)
admin.site.register(SchemaColumn, ColumnsAdmin)
admin.site.register(DataSetModel, SetsAdmin)
