from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.HomeDetails)
admin.site.register(models.DressSample)
admin.site.register(models.Queue)
admin.site.register(models.Pending)
admin.site.register(models.Served)
