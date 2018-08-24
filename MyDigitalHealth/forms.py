from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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


class CreateCardPackage(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
        )


class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
        )


class CreateCards(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'card_text',
        )


class CreateUserCardsort(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
        )
