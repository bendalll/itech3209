from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from cardsort.models import Package, Category, Card, UserCardsort


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


def create_category_formset(**kwargs):
    CategoryFormset = modelformset_factory(Category, fields=('category_name',), extra=kwargs['extra'])
    if 'package' in kwargs:
        new_category_formset = CategoryFormset(queryset=Category.objects.filter(package=kwargs['package']),
                                               prefix='category')
    else:
        new_category_formset = CategoryFormset(queryset=Category.objects.none(),
                                               prefix='category')
    return new_category_formset


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'card_text',
        )


def create_card_formset(**kwargs):
    CardFormset = modelformset_factory(Card, fields=('card_text',), extra=kwargs['extra'])
    if 'package' in kwargs:
        new_card_formset = CardFormset(queryset=Card.objects.filter(package=kwargs['package']), prefix='card')
    else:
        new_card_formset = CardFormset(queryset=Card.objects.none(), prefix='category')
    return new_card_formset


# note: if changing 'extra' also change the cardsort.js global var num_cards
CardsFormSet = modelformset_factory(Card, fields=('card_text',), extra=2)


class UserCardsortForm(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
            'user',
        )


def create_blank_form(num_categories, num_cards):
    """
    :return: a dict that can be passed as context to a template, which will render the forms to create a whole package
    including package name, categories, and cards
    """
    package_form = PackageForm()
    categories_formset = create_category_formset(extra=num_categories)
    cards_formset = create_card_formset(extra=num_cards)

    return {'package_form': package_form,
            'categories_formset': categories_formset,
            'cards_formset': cards_formset}


class BlankForm(forms.Form):
    def __init__(self, num_categories, num_cards):
        super().__init__()
        self.package_form = PackageForm()
        self.categories_formset = create_category_formset(extra=num_categories)
        self.cards_formset = create_card_formset(extra=num_cards)


def edit_package_form(package_id, **kwargs):
    """
    :return: a dict that can be passed as context to a template, which will render the forms pre-populated with the
    existing package's information, for editing
    """
    try:
        package = Package.objects.get(pk=package_id)
        package_form = PackageForm(instance=package)
        categories_formset = create_category_formset(package=package, extra=kwargs['extra'])
        cards_formset = CardsFormSet(queryset=Card.objects.filter(package=package), prefix='card')

    except ObjectDoesNotExist:
        print("The package you're looking for doesn't exist?")
        return {}

    return {'package_form': package_form,
            'categories_formset': categories_formset,
            'cards_formset': cards_formset,
            'exists_flag': True,  # processing flag to indicate that the package already exists
            'package_id': package_id}


def validate_and_create_package(request):
    package_form = PackageForm(request.POST)
    categories_formset = modelformset_factory(Category, fields=('category_name',))(request.POST,
                                                                                   request.FILES,
                                                                                   prefix='category')
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


def get_whole_package(package_id):
    active_package = Package.get_package_by_id(package_id)
    list_of_card_objects = Card.objects.filter(package=active_package)
    list_of_category_objects = Category.objects.filter(package=active_package)

    # Return items in dict for ease of processing
    package = {'package_id': package_id,
               'package_name': active_package.package_name,
               'cards': list_of_card_objects,
               'categories': list_of_category_objects
               }
    return package
