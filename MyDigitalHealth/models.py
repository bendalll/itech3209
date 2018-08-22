from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    card_text = models.CharField(max_length=200)
    admin_id = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'cards'


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    package_cards = models.ManyToManyField(Card)
    package_categories = models.TextField()
    package_owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner')
    assigned_users = models.ManyToManyField(User, related_name='assigned')
    user_editable_categories = models.BooleanField()

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Card_Package'

    @staticmethod
    def create_package(package_name):
        package = Package(package_name=package_name)
        package.save()
        return package


class AssignedPkg(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    package_id = models.ForeignKey(Package, on_delete=models.PROTECT)
    categories = models.TextField
    cards = models.ManyToManyField(Card)
    comment_text = models.TextField
