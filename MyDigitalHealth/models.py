from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    main_color = models.CharField(max_length=7, default='#337ab7')
    comments_allowed = models.BooleanField(default=True)
    user_defined_groups = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Packages'

    def get_groups(self):
        groups = Group.objects.filter(package=self)
        return groups

    def get_cards(self):
        cards = Card.objects.filter(package=self)
        return cards

    def to_dict(self):
        """ Used to return a package object as a dict, with package name, list of categories, and list of cards """
        list_of_group_objects = Group.objects.filter(package=self)
        list_of_card_objects = Card.objects.filter(package=self)

        package = {'package_id': self.pk,
                   'name': self.name,
                   'main_color': self.main_color,
                   'comments_allowed': self.comments_allowed,
                   'groups': list_of_group_objects,
                   'cards': list_of_card_objects,
                   'user_defined_groups' : self.user_defined_groups,
                   }
        return package


class Group(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Groups'


class Card(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    # group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text + "(#" + str(self.pk) + ")"

    class Meta:
        verbose_name_plural = 'Cards'


class SortedPackage(models.Model):
    parent_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="child_package")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, default='Placeholder')

    # TODO - Maybe add a manyToMany Field to make the sorted group info accessible on this object?

    def __str__(self):
        return "Sorted package for " + self.user.username

    # Return a list of unassigned cards
    def get_unassigned_cards(self):
        list_of_card_objects = Card.objects.filter(package=self.parent_package)
        list_of_group_objects = SortedGroup.objects.filter(sorted_package=self)

        # Create a set from the list of all cards in the parent package.
        sorted_cards = set(list_of_card_objects.all())

        # Iterate through the sorted groups and remove any cards which are already assigned a group.
        for group in list_of_group_objects:
            sorted_cards = sorted_cards - set(group.cards.all())
        return list(sorted_cards)

    def to_dict(self):
        """ Used to return a package object as a dict, with package name, list of categories, and list of cards """

        list_of_group_objects = SortedGroup.objects.filter(sorted_package=self)

        package = {'package_id': self.parent_package.pk,
                   'name': self.parent_package.name,
                   'main_color': self.parent_package.main_color,
                   'comments_allowed': self.parent_package.comments_allowed,
                   'comment': self.comment,
                   'groups': list_of_group_objects,
                   'cards': self.get_unassigned_cards(),
                   'user_defined_groups': self.parent_package.user_defined_groups,
                   }
        return package

    def get_groups(self):
        groups = SortedGroup.objects.filter(sorted_package=self)
        return groups

    def get_sort_progress(self):
        total_cards = len(Card.objects.filter(package=self.parent_package))
        unsorted_cards = len(self.get_unassigned_cards())
        return int(((total_cards-unsorted_cards)/total_cards)*100)

    class Meta:
        verbose_name_plural = 'Sorted_Packages'


class SortedGroup(models.Model):
    sorted_package = models.ForeignKey(SortedPackage, on_delete=models.CASCADE)
    parent_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cards = models.ManyToManyField(Card)

    class Meta:
        verbose_name_plural = "Sorted_Groups"


class Permission(models.Model):
    """ User Access Control for package assignation """
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
