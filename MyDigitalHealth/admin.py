from django.contrib import admin
from .models import Card_Packages, Card_Groups, Cards

# Register your models here.
admin.site.register(Card_Packages)
admin.site.register(Card_Groups)
admin.site.register(Cards)