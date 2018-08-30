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

# not using this form currently
class CreateForm(forms.ModelForm):
    """
    Form used to validate all data passed in from Create Package page before creating objects for db
    """
    package_name = forms.CharField()
    category_name = forms.CharField()
    card_text = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_names = CreateForm.objects.filter(
            profile=self.instance
        )
        for i in range(len(category_names) + 1):
            field_name = 'category_name%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = category_names[i].category_name
            except IndexError:
                    self.initial[field_name] = ""
            field_name = 'category_name%s' % (i + 1,)
            self.fields[field_name] = forms.CharField(required=False)
            self.fields[field_name] = ""

    def clean(self):
        category_names = set()
        i = 0
        field_name = 'category_name%s' % (i,)
        while self.cleaned_data.get(field_name):
            category_name = self.cleaned_data[field_name]
            if category_name in category_names:
                self.add_error(field_name, 'Duplicate')
            else:
                category_names.add(category_name)
            i += 1
            field_name = 'category_name%s' % (i,)
        self.cleaned_data["category_names"] = category_names

    # def save(self):
    #     package = self.instance
    #
    #     package.category_set.all().delete()
    #     for category_name in self.cleaned_data["category_names"]:
    #         CreateForm.objects.create(
    #             package=package,
    #             category_name="",
    #         )
    #     return True

# https://www.caktusgroup.com/blog/2018/05/07/creating-dynamic-forms-django/


class CreatePackageInitialForm(forms.Form):
    package_name = forms.CharField(max_length=200, label="Package Name")
    category_name_1 = forms.CharField(max_length=100, label="Category 1 Name")
    category_name_2 = forms.CharField(max_length=100, label="Category 2 Name")
    card_text_1 = forms.CharField(max_length=500, label="Card 1 Text")
    card_text_2 = forms.CharField(max_length=500, label="Card 2 Text")
    card_text_3 = forms.CharField(max_length=500, label="Card 3 Text")
    card_text_4 = forms.CharField(max_length=500, label="Card 4 Text")
