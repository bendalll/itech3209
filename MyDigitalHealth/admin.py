from django.contrib import admin
from .models import Card_Packages, Card_Groups, Cards, Comments, Sorted_Package

# Register your models here.
admin.site.register(Card_Packages)
admin.site.register(Card_Groups)
admin.site.register(Cards)
admin.site.register(Comments)
admin.site.register(Sorted_Package)