from django.contrib import admin
from .models import TimeReport, CSVData

# Register your models here.

admin.site.register(TimeReport)
admin.site.register(CSVData)