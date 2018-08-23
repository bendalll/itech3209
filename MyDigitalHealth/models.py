from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    package_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User.pk, on_delete=models.PROTECT)

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name_plural = 'Packages'

    @classmethod
    def create_package(cls, package_name, owner_id):
        new_package = Package(package_name=package_name, owner=owner_id)
        return new_package

    def save_package(self):
        # access the db and then save?
        self.save(force_insert=False, force_update=False)


class Category(models.Model):
    package_id = models.ForeignKey(Package.pk, on_delete=models.PROTECT)
    category_name = models.CharField(max_length=200)
    category_owner = models.ForeignKey(User.pk, on_delete=models.PROTECT)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'

    @classmethod
    def create_category(cls, category_name, category_owner):
        new_category = Category(category_name=category_name, category_owner=category_owner)
        return new_category

    def save_category(self):
        self.save(force_update=False, force_insert=False)


class Card(models.Model):
    package_id = models.ForeignKey(Package.pk, on_delete=models.PROTECT)
    category_id = models.ForeignKey(Category.pk, on_delete=models.PROTECT, default='1')
    card_text = models.CharField(max_length=200)

    def __str__(self):
        return self.card_text

    class Meta:
        verbose_name_plural = 'Cards'

    @classmethod
    def create_card(cls, package_id, card_text):
        new_card = Card(package_id=package_id, card_text=card_text)
        return new_card


class Comment(models.Model):
    package_id = models.ForeignKey(Package.pk, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User.pk, on_delete=models.PROTECT)
    comment_text = models.TextField(default='Placeholder')

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name_plural = 'Comments'

    @classmethod
    def create_comment(cls, package_id, user_id, comment_text):
        new_comment = Comment(package_id=package_id, user_id=user_id, comment_text=comment_text)
        return new_comment
