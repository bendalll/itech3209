from django.contrib import admin
from .models import Package, Category, Card, Comment

# Register your models here.
admin.site.register(Package)
admin.site.register(Category)
admin.site.register(Card)
admin.site.register(Comment)
