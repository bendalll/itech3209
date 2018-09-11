from django import forms
from django.forms import modelformset_factory
from cardsort.models import Package, Category, Card, UserCardsort


class PackageNameForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
        )


class UserCardsortForm(forms.ModelForm):
    class Meta:
        model = UserCardsort
        fields = (
            'comment_text',
            'user',
        )


def create_category_formset(**kwargs):
    """ Function to create and return a model formset of Category Forms tailored to the context of the calling code """

    # Filter for 'extra' here to avoid always having to specify extra=0
    if 'extra' in kwargs:
        CategoryFormset = modelformset_factory(Category, fields=('category_name',), extra=kwargs['extra'])
    else:
        CategoryFormset = modelformset_factory(Category, fields=('category_name',))

    if 'package' in kwargs:
        new_category_formset = CategoryFormset(queryset=Category.objects.filter(package=kwargs['package']),
                                               prefix='category')
    elif 'request' in kwargs:
        new_category_formset = CategoryFormset(kwargs['request'].POST, kwargs['request'].FILES, prefix='category')
    else:
        new_category_formset = CategoryFormset(queryset=Category.objects.none(), prefix='category')

    return new_category_formset


def create_card_formset(**kwargs):
    """ Function to create and return and model formset of Card Forms tailored to the context of the calling code """

    # Filter for 'extra' here to avoid always having to specify extra=0
    if 'extra' in kwargs:
        CardFormset = modelformset_factory(Card, fields=('card_text',), extra=kwargs['extra'])
    else:
        CardFormset = modelformset_factory(Card, fields=('card_text',))

    if 'package' in kwargs:
        new_card_formset = CardFormset(queryset=Card.objects.filter(package=kwargs['package']), prefix='card')
    elif 'request' in kwargs:
        new_card_formset = CardFormset(kwargs['request'].POST, kwargs['request'].FILES, prefix='card')
    else:
        new_card_formset = CardFormset(queryset=Card.objects.none(), prefix='card')

    return new_card_formset


def validate_and_save_package(request, **kwargs):
    """
    Take POST data and create forms/formsets to validate, then use cleaned valid data to create new objects
    :param request:
    :param kwargs: if an existing package is passed in via package_id, existing package is edited instead of creating
    a new package
    :return: the newly created or edited package
    """
    package_form = PackageNameForm(request.POST)
    categories_formset = create_category_formset(request=request)
    cards_formset = create_card_formset(request=request)
    if package_form.is_valid() and categories_formset.is_valid() and cards_formset.is_valid():
        if 'package_id' in kwargs:
            package = save_edited_package(kwargs['package_id'],
                                          package_form.cleaned_data,
                                          categories_formset.cleaned_data,
                                          cards_formset.cleaned_data)
        else:
            package = create_new_package(package_form.cleaned_data,
                                         categories_formset.cleaned_data,
                                         cards_formset.cleaned_data,
                                         request.user)
        return package
    else:
        return "Form data invalid?"


def create_new_package(package_form_cleaned, categories_form_cleaned, cards_form_cleaned, owner):
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


def save_edited_package(package_id, package_form_cleaned, categories_form_cleaned, cards_form_cleaned):
    """
    Retrieve a Package and associated Card and Category objects and save over using cleaned form data
    :param package_id: the ID of the package that was edited
    :param package_form_cleaned: the POST data from the form after cleaned()
    :param categories_form_cleaned: the POST data from the form after cleaned();
        a dict with each form submitted with a category_name and id (None)
    :param cards_form_cleaned: as above categories_form_cleaned but for cards
    :return: a new package, already saved
    """
    edited_package = Package.objects.get(pk=package_id)
    edited_package.package_name = package_form_cleaned['package_name']
    edited_package.save()

    for each in categories_form_cleaned:
        edited_category = Category.objects.get(pk=each['id'].pk)  # don't know why the id is the whole object!
        edited_category.category_name = each['category_name']
        edited_category.save()

    for each in cards_form_cleaned:
        edited_card = Card.objects.get(pk=each['id'].pk)  # as above
        edited_card.card_text = each['card_text']
        edited_card.save()

    return edited_package


class NewPackageForm(forms.Form):
    """ *UNUSED IN EXAMPLE CODE*
    Class to create a blank form for making a package, with the forms / formsets as attributes of the BlankForm object
    """
    def __init__(self, num_categories, num_cards):
        super().__init__()
        self.package_form = PackageNameForm()
        self.categories_formset = create_category_formset(extra=num_categories)
        self.cards_formset = create_card_formset(extra=num_cards)

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_form': self.package_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset}
        return package


class EditPackageForm(forms.Form):
    """
    Currently not used. Create a pre-filled form object that can be rendered to edit an existing package
    Required: validate package_id before init!
    """
    def __init__(self, package_id):
        super().__init__()
        package = Package.objects.get(pk=package_id)
        self.package_form = PackageNameForm(instance=package)
        self.categories_formset = create_category_formset(package=package)
        self.cards_formset = create_card_formset(package=package)
        self.exists_flag = True
        self.package_id = package_id

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_form': self.package_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset,
                   'exists_flag': self.exists_flag,
                   'package_id': self.package_id}
        return package


#  Unused code
# def edit_package_form(package_id, num_categories=0, num_cards=0):
#     """
#     :return: a dict that can be passed as context to a template, which will render the forms pre-populated with the
#     existing package's information, for editing
#     """
#     try:
#         package = Package.objects.get(pk=package_id)
#     except ObjectDoesNotExist:
#         print("These aren't the droids you're looking for")
#         return {}
#
#     package_form = PackageNameForm(instance=package)
#     categories_formset = create_category_formset(package=package, extra=num_categories)
#     cards_formset = create_card_formset(package=package, extra=num_cards)
#
#     return {'package_form': package_form,
#             'categories_formset': categories_formset,
#             'cards_formset': cards_formset,
#             'exists_flag': True,  # processing flag to indicate that the package already exists
#             'package_id': package_id}
#
# def create_blank_form(num_categories=2, num_cards=6):
#     """
#     :return: a dict that can be passed as context to a template, which will render the forms to create a whole package
#     including package name, categories, and cards
#     """
#     package_form = PackageNameForm()
#     categories_formset = create_category_formset(extra=num_categories)
#     cards_formset = create_card_formset(extra=num_cards)
#
#     return {'package_form': package_form,
#             'categories_formset': categories_formset,
#             'cards_formset': cards_formset}
