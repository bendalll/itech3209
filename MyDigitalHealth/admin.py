from django.contrib import admin
from .models import Package, Group, Card, SortedPackage

admin.site.register(Package)
admin.site.register(Group)
admin.site.register(Card)
admin.site.register(SortedPackage)
