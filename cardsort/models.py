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


class SortedCategory(models.Model):
    """ Class to represent a link between a card and a category """
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cards = models.ManyToManyField(Card)

    def __init__(self, pk_for_self, category_id, *args, **kwargs):
        super().__init__()
        self.pk = pk_for_self
        self.category = Category.objects.get(pk=category_id)
        self.save()
        if 'card_ids' in kwargs:
            for card_id in kwargs['card_ids']:
                card = Card.objects.get(pk=card_id)
                self.cards.add(card)

    def __str__(self):
        return "Sorted cards for %s" % self.category.category_name
        # TODO: this

    def add_cards(self, card_ids):
        for card_id in card_ids:
            card = Card.objects.get(pk=card_id)
            self.cards.add(card)


class UserCardsort(models.Model):
    """ Represents a saved version of a package, as assigned to a user, holding their comment data and sorted
    card-category associations"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # change to CASCADE if delete save when delete user
    comment_text = models.TextField(default='placeholder text')
    sorted_category = models.ManyToManyField(SortedCategory)

    def __str__(self):
        return "Saved sort for user: %s package" % self.user

    def to_dict(self):
        """ Used to return a saved package object as a dict, with package name, list of categories,
         and list of cards with the category they are saved in """

        list_of_category_objects = self.sorted_category.all()
        list_of_card_objects = Card.objects.filter(package=self)

        # unassigned cards will be
        # set > difference - set of categories vs package cards

        package = {'package_id': self.package.pk,
                   'package_name': self.package.package_name,
                   'categories': list_of_category_objects,
                   'cards': list_of_card_objects,
                   }
        return package

    class Meta:
        verbose_name_plural = 'Saved Packages'
