from django.contrib import admin
from .models import Package, Card, AssignedPkg

# Register your models here.
admin.site.register(Package)
admin.site.register(Card)
admin.site.register(AssignedPkg)
