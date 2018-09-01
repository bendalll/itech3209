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


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'card_text',
        )


class UserCardsortForm(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
            'user',
        )


class PackageSubmittedForm(forms.Form):
    package_name = forms.CharField(max_length=200, label="Package Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("My things are: ", self.fields)

        # for i in range(len(12) + 1):
        #     field_name = 'cateogry_%s' % (i,)
        #     self.fields[field_name] = forms.CharField(required=True)
        #     try:
        #         self.initial[field_name] = categories[i].category_name
        #     except IndexError:
        #         self.initial[field_name] = ''
        # field_name = 'category_%s' % (i + 1,)
        # self.fields[field_name] = forms.CharField(required=False)
        # self.fields[field_name] = ''

    def get_category_names(self):
        for field_name in self.fields:
            if field_name.startswith('category_'):
                yield self[field_name]

    # Iterate over the category_name items to create categories

    # Iterate over the card_id items to create cards
