from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Package, Category, Card, Comment


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


class CreateCardGroup(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'package_id',
            'category_name',
        )


class CreateCards(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'package_id',
            'card_text',
        )


class CreateComments(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'package_id',
            'user_id',
            'comment_text',
        )
