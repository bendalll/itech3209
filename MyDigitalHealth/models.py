from django.db import models

class Card_Packages(models.Model):
	name = models.CharField(max_length=200)
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
	text = models.CharField(max_length=200)	
	def __str__(self):
		return self.text
	class Meta:
		verbose_name_plural = 'Cards'
	
