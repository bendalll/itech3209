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


class Sorted_Packages(Card_Packages):
    parent_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE, related_name='base_package')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, default='Placeholder')

    def __str__(self):
        return "Sorted" + self.name + " for " + self.user.username

    class Meta:
        verbose_name_plural = 'Sorted_Packages'


class Card_Groups(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Card_Groups'


class Cards(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    card_group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Cards'


class Permissions(models.Model):
    """ User Access Control for package assignation """
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
