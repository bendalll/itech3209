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


class CreatePackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
        )


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'category_name',
        )


class CreateCardForm(forms.ModelForm):
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
            'user',
        )


class CreateForm(forms.Form):
    """
    Form used to validate all data passed in from Create Package page before creating objects for db
    """
    package_name = forms.CharField()
    category_name = forms.CharField()
    card_text = forms.CharField()
