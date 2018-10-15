from django.db import models
from django.contrib.auth.models import User


class Card_Packages(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    main_color = models.CharField(max_length=7, default='#337ab7')
    comments_allowed = models.BooleanField(default=True)
    user_defined_groups = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Card_Packages'

    def get_groups(self):
        groups = Card_Groups.objects.filter(card_package=self)
        return groups

    def get_cards(self):
        cards = Cards.objects.filter(card_package=self)
        return cards

    def to_dict(self):
        """ Used to return a package object as a dict, with package name, list of categories, and list of cards """
        list_of_group_objects = Card_Groups.objects.filter(card_package=self)
        list_of_card_objects = Cards.objects.filter(card_package=self)

        package = {'package_id': self.pk,
                   'name': self.name,
                   'main_color': self.main_color,
                   'comments_allowed': self.comments_allowed,
                   'card_groups': list_of_group_objects,
                   'cards': list_of_card_objects,
                   }
        return package


class Card_Groups(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Card_Groups'


class Cards(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    #card_group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text + "(#" + str(self.pk) + ")"

    class Meta:
        verbose_name_plural = 'Cards'

class Sorted_Groups(models.Model):
    sorted_package = models.ForeignKey('Sorted_Packages', on_delete=models.CASCADE)
    parent_group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cards = models.ManyToManyField(Cards)


class Sorted_Packages(models.Model):
    parent_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE, related_name="child_package")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, default='Placeholder')

    #TODO - Maybe add a manyToMany Field to make the sorted group info accessible on this object?

    def __str__(self):
        return "Sorted" + self.name + " for " + self.user.username

    def to_dict(self):
        """ Used to return a package object as a dict, with package name, list of categories, and list of cards """

        list_of_group_objects = Sorted_Groups.objects.filter(sorted_package=self)
        list_of_card_objects = Cards.objects.filter(card_package=self.parent_package)

        # Create a set from the list of all cards in the parent package.
        sortedcards = set(list_of_card_objects.all())

        # Iterate through the sorted groups and remove any cards which are already assigned a group.
        for group in list_of_group_objects:
            sortedcards = sortedcards - set(group.cards.all())

        package = {'package_id': self.parent_package.pk,
                   'name': self.parent_package.name,
                   'main_color': self.parent_package.main_color,
                   'comments_allowed': self.parent_package.comments_allowed,
                   'comment': self.comment,
                   'card_groups': list_of_group_objects,
                   'cards': list(sortedcards),
                   }
        return package

    class Meta:
        verbose_name_plural = 'Sorted_Packages'



class Permissions(models.Model):
    """ User Access Control for package assignation """
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
