from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.person)
admin.site.register(models.service)
admin.site.register(models.service_type)
admin.site.register(models.exercise)
admin.site.register(models.booking)