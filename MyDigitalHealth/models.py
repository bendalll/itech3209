from django.db import models
from django.contrib.auth.models import User


class Card_Packages(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Card_Packages'


class Card_Groups(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Card_Groups'


class Cards(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.PROTECT)
    card_group = models.ForeignKey(Card_Groups, on_delete=models.PROTECT, default='1')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Cards'


class Comments(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, default='Placeholder')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name_plural = 'Comments'
