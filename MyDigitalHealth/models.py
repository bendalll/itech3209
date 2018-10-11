from django.db import models
from django.contrib.auth.models import User


class Card_Packages(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    main_color = models.CharField(max_length=7, default='#337ab7')
    comments_allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Card_Packages'


class Card_Groups(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Card_Groups'


class Cards(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    card_group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE, default='1')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Cards'


class Comments(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, default='Placeholder')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name_plural = 'Comments'


class Sorted_Package(models.Model):
    card_package = models.ForeignKey(Card_Packages, on_delete=models.CASCADE)
    card_group = models.ForeignKey(Card_Groups, on_delete=models.CASCADE, default='1')
    cards = models.ManyToManyField(Cards)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Sorted_Packages'
