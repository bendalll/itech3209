from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Packages'

    def get_categories(self):
        categories = Category.objects.filter(package=self)
        return categories

    def get_cards(self):
        cards = Card.objects.filter(package=self)
        return cards

    def to_dict(self):
        """ Used to return a package object as a dict, with package name, list of categories, and list of cards """
        list_of_category_objects = Category.objects.filter(package=self)
        list_of_card_objects = Card.objects.filter(package=self)

        package = {'package_id': self.pk,
                   'package_name': self.package_name,
                   'categories': list_of_category_objects,
                   'cards': list_of_card_objects,
                   }
        return package


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
    """ Represents a saved version of a package, as assigned to a user, holding their comment data and sorted
    card-category associations"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # change to CASCADE if delete save when delete user
    sortlist = {
        models.ForeignKey(Card, on_delete=models.CASCADE): models.ForeignKey(Category, on_delete=models.CASCADE)
    }
    comment_text = models.TextField(default='placeholder text')

    def __str__(self):
        return "Saved information for user ", self.user_id
        # TODO make this more meaningful

    class Meta:
        verbose_name_plural = 'Saved Packages'
