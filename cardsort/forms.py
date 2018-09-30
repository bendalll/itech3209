from django import forms
from django.forms import modelformset_factory, TextInput
from cardsort.models import Package, Category, Card


class PackageBaseForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
            'main_color',
        )
        widgets = {
            'main_color': TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'main_color': 'Color of category headings'
        }


class PackageForm(forms.Form):
    """
    Class to create a blank form for making a package, with the forms / formsets as attributes of the BlankForm object
    """
    NEW_PACKAGE_FLAG = -1

    def __init__(self, package_id=NEW_PACKAGE_FLAG, num_categories=2, num_cards=4):
        """
        :param package_id: ID of the package to be edited with this form, or, default to -1 to represent new package
        :param num_categories: initial number of categories to include with form; default as 2
        :param num_cards: initial number of cards to include with form; default as 4
        """
        if package_id == self.NEW_PACKAGE_FLAG:
            super().__init__()
            self.package_base_form = PackageBaseForm()
            self.categories_formset = create_category_formset(extra=num_categories)
            self.cards_formset = create_card_formset(extra=num_cards)
            self.package_id = self.NEW_PACKAGE_FLAG
        else:
            super().__init__()
            package = Package.objects.get(pk=package_id)
            self.package_base_form = PackageBaseForm(instance=package)
            self.categories_formset = create_category_formset(package=package)
            self.cards_formset = create_card_formset(package=package)
            self.package_id = package_id

    def __str__(self):
        return "Form to create or edit a package"

    def to_dict(self):
        #TODO UPDATE
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_base_form': self.package_base_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset,
                   'package_id': self.package_id}
        return package


# class EditPackageForm(forms.Form):
#     """
#     Currently not used. Create a pre-filled form object that can be rendered to edit an existing package
#     Required: validate package_id before init?
#     """
#     def __init__(self, package_id):
#         super().__init__()
#         package = Package.objects.get(pk=package_id)
#         self.package_form = PackageBaseForm(instance=package)
#         self.categories_formset = create_category_formset(package=package)
#         self.cards_formset = create_card_formset(package=package)
#         self.package_id = package_id
#
#     def __str__(self):
#         return "Edit form for ", self.package_form.package_name
#
#     def to_dict(self):
#         """ Get the Form as a dict that is easy to pass through as context for template to render """
#         package = {'package_form': self.package_form,
#                    'categories_formset': self.categories_formset,
#                    'cards_formset': self.cards_formset,
#                    'package_id': self.package_id}
#         return package


class SubmittedForm(forms.Form):
    """ Class used to create a new package or save an edited package by validating form data """
    def __init__(self, request):
        super().__init__()
        self.package_base_form = PackageBaseForm({'package_name': request.POST['package_name'],
                                             'main_color': request.POST['main_color']})
        self.categories_formset = create_category_formset(request=request)
        self.cards_formset = create_card_formset(request=request)
        self.owner = request.user
        self.package_id = request.POST['package_id']

    def is_valid(self):
        """ Validate each of the included forms in the collected form object """
        if self.package_base_form.is_valid() and self.categories_formset.is_valid() and self.cards_formset.is_valid():
            return True
        else:
            return False

    def save(self):
        """
        If the package was being edited, retrieve the existing items and update them; otherwise, create new ones
        :return: the new or edited package
        """
        if int(self.package_id) == -1:  # TODO: better way to do this? -1 means new package means create new package
            package = Package(package_name=self.package_base_form.cleaned_data['package_name'],
                              main_color=self.package_base_form.cleaned_data['main_color'],
                              owner=self.owner)
            package.save()
        else:
            package = Package.objects.get(pk=self.package_id)
            package.package_name = self.package_base_form.cleaned_data['package_name']
            package.main_color = self.package_base_form.cleaned_data['main_color']
            package.save()
            # easiest to delete all the existing data and create it again
            for category in package.get_categories():
                category.delete()
            for card in package.get_cards():
                card.delete()

        for category in self.categories_formset.cleaned_data:
            category_name = category['category_name']
            new_category = Category(category_name=category_name, package=package)
            new_category.save()

        for card in self.cards_formset.cleaned_data:
            card_text = card['card_text']
            new_card = Card(card_text=card_text, package=package)
            new_card.save()

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

    for form in new_category_formset:
        form.empty_permitted = False

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

    for form in new_card_formset:
        form.empty_permitted = False

    return new_card_formset
