from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

from .models import Package, Category, Card, UserCardsort


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'category_name',
        )


# note: if changing 'extra' also change the cardsort.js global var num_categories
CategoriesFormSet = modelformset_factory(Category, fields=('category_name',), extra=2)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'card_text',
        )


# note: if changing 'extra' also change the cardsort.js global var num_cards
CardsFormSet = modelformset_factory(Card, fields=('card_text',), extra=4)


class UserCardsortForm(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
            'user',
        )
