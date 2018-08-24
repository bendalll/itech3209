from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Packages'

    @classmethod
    def get_package_by_id(cls, package_id):
        package = Package.objects.get(id__exact=package_id)
        return package

    @classmethod
    def get_packages_by_owner(cls, owner):
        packages_list = Package.objects.filter(owner_id=owner.id)
        return packages_list

    @staticmethod
    def get_package_categories(self):
        categories = Category.objects.filter(self.pk)
        return categories

    @staticmethod
    def get_package_cards(self):
        cards = Card.objects.filter(package=self)
        return cards


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Card(models.Model):
    card_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'Cards'


class UserCardsort(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # change to CASCADE if delete save when delete user
    sortlist = {
        models.ForeignKey(Card, on_delete=models.PROTECT): models.ForeignKey(Category, on_delete=models.PROTECT)
    }
    comment_text = models.TextField(default='placeholder text')
