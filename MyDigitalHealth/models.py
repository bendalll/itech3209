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
        package = Package.objects.get(pk=package_id)
        return package

    @classmethod
    def get_packages_by_owner(cls, owner):
        packages_list = Package.objects.filter(owner_id=owner.id)
        return packages_list

    @classmethod
    def get_package_categories(cls, package_id):
        categories = Category.objects.filter(pk=package_id)
        return categories

    @classmethod
    def get_package_cards(cls, package_id):
        cards = Card.objects.filter(pk=package_id)
        return cards


class Category(models.Model):
    """ Represents a category within a package into which Cards are sorted """
    category_name = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Card(models.Model):
    """ Represents a card within a package which is sorted into a category"""
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

    def __str__(self):
        return self.user_id
        # TODO make this more meaningful

    class Meta:
        verbose_name_plural = 'Saved Packages'
