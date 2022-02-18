# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

from django.apps import apps
app = apps.get_app_config('browser')
# Register your models here.
class MultiDBModelAdmin(admin.ModelAdmin):
	# A handy constant for the name of the alternate database.
	#using='naviremote'
	using = 'alx_narciarze'
	def __init__(self, model, admin_site):# *args, **kwargs):
		self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
		#self.list_filter = [field.name for field in model._meta.fields if field.name != "id"]
		#self.search_fields = [field.name for field in model._meta.fields if field.name != "id"]
		super(MultiDBModelAdmin, self).__init__(model,admin_site)#*args, **kwargs)
	def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
		obj.save(using=self.using)
	def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
		obj.delete(using=self.using)
	def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
		return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
		return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
	def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
		return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
		

for model_name, model in app.models.items():
    admin.site.register(model, MultiDBModelAdmin)

