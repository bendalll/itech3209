from django.contrib import admin
from cardsort.models import Package, Category, Card, UserSavedPackage

# Register your models here.
admin.site.register(Package)
admin.site.register(Category)
admin.site.register(Card)
admin.site.register(UserSavedPackage)
