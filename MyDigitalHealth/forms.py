from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
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
CardsFormSet = modelformset_factory(Card, fields=('card_text',), extra=2)


class UserCardsortForm(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
            'user',
        )


def create_blank_form():
    """
    :return: a dict that can be passed as context to a template, which will render the forms to create a whole package
    including package name, categories, and cards
    """
    package_form = PackageForm()
    categories_formset = CategoriesFormSet(queryset=Category.objects.none(), prefix='category')
    cards_formset = CardsFormSet(queryset=Card.objects.none(), prefix='card')

    return {'package_form': package_form,
            'categories_formset': categories_formset,
            'cards_formset': cards_formset}


def edit_package_form(package_id):
    """
    :return: a dict that can be passed as context to a template, which will render the forms pre-populated with the
    existing package's information, for editing
    """
    try:
        package = Package.objects.get(pk=package_id)
        package_form = PackageForm(instance=package)
        categories_formset = CategoriesFormSet(queryset=Category.objects.filter(package=package), prefix='category')
        print(categories_formset)
        cards_formset = CardsFormSet(queryset=Card.objects.filter(package=package), prefix='card')

    except ObjectDoesNotExist:
        print("Something went very wrong here")
        return {}

    return {'package_form': package_form,
            'categories_formset': categories_formset,
            'cards_formset': cards_formset}


def validate_and_create_package(request):
    # TODO: method receives request.POST data and validates it before calling create()
    package_form = PackageForm(request.POST)
    categories_formset = CategoriesFormSet(request.POST, request.FILES, prefix='category')
    cards_formset = CardsFormSet(request.POST, request.FILES, prefix='card')
    if package_form.is_valid() and categories_formset.is_valid() and cards_formset.is_valid():
        new_package = create_package(package_form.cleaned_data,
                             categories_formset.cleaned_data,
                             cards_formset.cleaned_data,
                             request.user)
        return new_package
    else:
        return "Form data invalid?"


def create_package(package_form_cleaned, categories_form_cleaned, cards_form_cleaned, owner):
    """
    Create a new Package and associated Card and Category objects using cleaned form data
    :param package_form_cleaned: the POST data from the form after cleaned()
    :param categories_form_cleaned: the POST data from the form after cleaned();
        a dict with each form submitted with a category_name and id (None)
    :param cards_form_cleaned: as above categories_form_cleaned but for cards
    :param owner: the request.user; logged in admin who will own the card package once created
    :return: a new package, already saved
    """
    package_name = package_form_cleaned['package_name']
    new_package = Package(package_name=package_name, owner=owner)
    new_package.save()

    for each in categories_form_cleaned:
        category_name = each['category_name']
        new_category = Category(category_name=category_name, package=new_package)
        new_category.save()

    for each in cards_form_cleaned:
        card_text = each['card_text']
        new_card = Card(card_text=card_text, package=new_package)
        new_card.save()

    return new_package
