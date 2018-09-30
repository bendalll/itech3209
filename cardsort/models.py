from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    main_color = models.CharField(max_length=7, default='#337ab7')
    type = "Base Package"

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

    def assign(self):
        """ Method to duplicate the package as an AssignedPackage """
        assigned_package = AssignedPackage(package_name=self.package_name, owner=self.owner, comment_text="")
        assigned_package.save()
        # Base Packages have no blank "Cards" default category, so we need to add it here
        first_category = Category(category_name="Cards", package=assigned_package)
        first_category.save()
        for category in self.get_categories():
            new_category = Category(category_name=category.category_name, package=assigned_package)
            new_category.save()
        for card in self.get_cards():
            # Assign all cards to the default first_category
            new_card = Card(card_text=card.card_text, package=assigned_package, category=first_category)
            new_card.save()
        return assigned_package


class AssignedPackage(Package):
    """ Represents a Package in a state where it is owned by a user """
    comment_text = models.TextField(default='')
    type = "Assigned Package"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "Assigned Package"

    class Meta:
        verbose_name_plural = 'Assigned Packages'

    def __str__(self):
        return "%s assigned to user" % self.package_name

    def to_dict(self):
        """ Used to return a saved package object as a dict for easy context rendering """
        assigned_package = {'package_id': self.pk,
                            'package_name': self.package_name,
                            'categories': self.get_categories(),
                            'cards': self.get_cards(),
                            'comment': self.comment_text
                            }
        return assigned_package


class Category(models.Model):
    """ Represents a category within a package into which Cards are sorted """
    category_name = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_cards(self):
        cards = Card.objects.filter(category=self)
        return cards


class Card(models.Model):
    """ Represents a card within a package which is sorted into a category"""
    card_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'Cards'


class UserSavedPackage(models.Model):
    """ Represents the instance of a package as assigned to a user """
    base_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="base_package")
    assigned_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="user_package")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Saved Packages'

    def __str__(self):
        return "Saved package %s for %s" % (self.assigned_package, self.user)
