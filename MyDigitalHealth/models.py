from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    package_cards = ListCharField
    package_categories = ListCharField
    package_owner = models.ForeignKey
    assigned_users = ListCharField
    user_editable_categories = False

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Card_Package'

    @staticmethod
    def create_package(package_name):
        package = Package(package_name=package_name)
        package.save()
        return package


class Card(models.Model):
    card_text = models.CharField(max_length=200)
    admin_id = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'cards'


class AssignedPkg(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    package_id = models.ForeignKey(Package, on_delete=models.PROTECT)
    categories = ListCharField
    cards = ListCharField
    comment_text = models.TextField

# Used to use Category table:
# class Category(models.Model):
#     card_package = models.ForeignKey(Package, on_delete=models.PROTECT)
#     title = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'category'
