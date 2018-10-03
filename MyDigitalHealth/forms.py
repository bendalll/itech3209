from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from .models import Card_Packages, Card_Groups, Cards, Comments


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
        model = Card_Packages
        fields = (
            'name',
            'main_color',
            'comments_allowed',
        )
        labels = {
            'main_color': "Colour of Group Headings"
        }
        widgets = {
            'main_color': TextInput(attrs={'type': 'color', 'onchange': 'changeHeadingColor()'})
        }


class CreateCardGroup(forms.ModelForm):
    class Meta:
        model = Card_Groups
        fields = (
            'card_package',
            'title',
        )


class CreateCards(forms.ModelForm):
    class Meta:
        model = Cards
        fields = (
            'card_package',
            'text',
        )


class CreateComments(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'card_package',
            'comment',
            )
