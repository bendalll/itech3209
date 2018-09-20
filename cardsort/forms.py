from django import forms
from django.forms import modelformset_factory
from cardsort.models import Package, Category, Card, UserSavedPackage


class PackageNameForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
        )


class UserSaveForm(forms.ModelForm):
    class Meta:
        model = UserSavedPackage
        fields = (
            'user',
        )


class NewPackageForm(forms.Form):
    """
    Class to create a blank form for making a package, with the forms / formsets as attributes of the BlankForm object
    """
    def __init__(self, num_categories=2, num_cards=4):
        """
        :param num_categories: initial number of categories to include with form; default as 2
        :param num_cards: initial number of cards to include with form; default as 4
        """
        super().__init__()
        self.package_form = PackageNameForm()
        self.categories_formset = create_category_formset(extra=num_categories)
        self.cards_formset = create_card_formset(extra=num_cards)

    def __str__(self):
        return "Form to create a new package"

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_form': self.package_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset}
        return package


class EditPackageForm(forms.Form):
    """
    Currently not used. Create a pre-filled form object that can be rendered to edit an existing package
    Required: validate package_id before init?
    """
    def __init__(self, package_id):
        super().__init__()
        package = Package.objects.get(pk=package_id)
        self.package_form = PackageNameForm(instance=package)
        self.categories_formset = create_category_formset(package=package)
        self.cards_formset = create_card_formset(package=package)
        self.package_id = package_id

    def __str__(self):
        return "Edit form for ", self.package_form.package_name

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_form': self.package_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset,
                   'package_id': self.package_id}
        return package


class SubmittedForm(forms.Form):
    """ Class used to create a new package or save an edited package by validating form data """
    def __init__(self, request):
        super().__init__()
        self.package_form = PackageNameForm({'package_name': request.POST['package_name']})
        self.categories_formset = create_category_formset(request=request)
        self.cards_formset = create_card_formset(request=request)
        self.owner = request.user
        if 'package_id' in request.POST:
            self.package_id = request.POST['package_id']

    def is_valid(self):
        """ Validate each of the included forms in the collected form object """
        if self.package_form.is_valid() and self.categories_formset.is_valid() and self.cards_formset.is_valid():
            return True
        else:
            return False

    def save(self):
        """
        If the package was being edited, retrieve the existing items and update them; otherwise, create new ones
        :return: the new or edited package
        """
        if hasattr(self, 'package_id'):  # TODO: better way to do this?
            existing_package = Package.objects.get(pk=self.package_id)
            existing_package.delete()
            new_package = Package(package_name=self.package_form.cleaned_data['package_name'], owner=self.owner)
            new_package.save()
        else:
            new_package = Package(package_name=self.package_form.cleaned_data['package_name'], owner=self.owner)
            new_package.save()

        for category in self.categories_formset.cleaned_data:
            category_name = category['category_name']
            new_category = Category(category_name=category_name, package=new_package)
            new_category.save()

        for card in self.cards_formset.cleaned_data:
            card_text = card['card_text']
            new_card = Card(card_text=card_text, package=new_package)
            new_card.save()

        package = new_package

        # Return either the new package or edited package
        return package


def create_category_formset(**kwargs):
    """ Function to create and return a model formset of Category Forms tailored to the context of the calling code """

    # Filter for 'extra' here to avoid always having to specify extra=0
    if 'extra' in kwargs:
        CategoryFormset = modelformset_factory(Category, fields=('category_name',), extra=kwargs['extra'])
    else:
        CategoryFormset = modelformset_factory(Category, fields=('category_name',), extra=0)

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
        CardFormset = modelformset_factory(Card, fields=('card_text',), extra=0)

    if 'package' in kwargs:
        new_card_formset = CardFormset(queryset=Card.objects.filter(package=kwargs['package']), prefix='card')
    elif 'request' in kwargs:
        new_card_formset = CardFormset(kwargs['request'].POST, kwargs['request'].FILES, prefix='card')
    else:
        new_card_formset = CardFormset(queryset=Card.objects.none(), prefix='card')

    return new_card_formset
