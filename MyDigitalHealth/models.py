from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Packages'


class Category(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.PROTECT)
    category_name = models.CharField(max_length=200)
    category_owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Card(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.PROTECT)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, default='1')
    card_text = models.CharField(max_length=200)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'Cards'


class Comment(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.TextField(default='Placeholder')

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name_plural = 'Comments'
