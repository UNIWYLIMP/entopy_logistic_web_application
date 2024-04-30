from django.contrib import admin
from .models import *

models = [CustomUser, DeliveryCompany]

# Register your models here.
admin.site.register(models)
