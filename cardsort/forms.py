from django import forms
from django.forms import modelformset_factory, TextInput
from cardsort.models import Package, Category, Card


class PackageBaseForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'package_name',
            'main_color',
            'comments_enabled',
        )
        widgets = {
            'main_color': TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'main_color': 'Color of category headings',
            'comments_enabled': 'Enable comments',
        }


class PackageForm(forms.Form):
    """
    Class to create a blank form for making a package, and create a new package object when submitted, or save edits in
    the database
    """
    NEW_PACKAGE_FLAG = -1
    num_categories = 2  # default the number of category name input fields to this
    num_cards = 4  # default the number of card text input fields to this

    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'request' in kwargs:
            """ Checks whether the form is being created with POST data, and so populates it with that data in
            preparation for validation """
            request = kwargs['request']
            # Create a form with the POST data, to be validated
            if 'comments_enabled' in request.POST:
                comments_enabled = True
            else:
                comments_enabled = False
            self.package_base_form = PackageBaseForm({'package_name': request.POST['package_name'],
                                                      'main_color': request.POST['main_color'],
                                                      'comments_enabled': comments_enabled})
            self.categories_formset = create_category_formset(request=request)
            self.cards_formset = create_card_formset(request=request)
            self.owner = request.user
            self.package_id = request.POST['package_id']

        elif 'package_id' in kwargs and kwargs['package_id'] != -1:
            """ Checks whether the form is being created to edit a given package, and so populates it with the package
            information so it can be edited """
            package = Package.objects.get(pk=kwargs['package_id'])
            self.package_base_form = PackageBaseForm(instance=package)
            self.categories_formset = create_category_formset(package=package)
            self.cards_formset = create_card_formset(package=package)
            self.package_id = kwargs['package_id']
        else:
            """ Default to create a new, blank form, with the default number of category and card inputs, to create a
            new package """
            self.package_base_form = PackageBaseForm()
            if 'num_categories' in kwargs:
                self.num_categories = kwargs['num_categories']
            if 'num_cards' in kwargs:
                self.num_cards = kwargs['num_cards']

            self.categories_formset = create_category_formset(extra=self.num_categories)
            self.cards_formset = create_card_formset(extra=self.num_cards)
            self.package_id = self.NEW_PACKAGE_FLAG

    def __str__(self):
        return "Form to create, edit, or submit a package or package information"

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_base_form': self.package_base_form,
                   'categories_formset': self.categories_formset,
                   'cards_formset': self.cards_formset,
                   'package_id': self.package_id}
        return package

    def is_valid(self):
        """ Validate each of the included forms/formsets in the collected form object """
        if self.package_base_form.is_valid():
            if self.categories_formset.is_valid():
                if self.cards_formset.is_valid():
                    return True
                else:
                    print("Cards formset is invalid")
            else:
                print("Category formset is invalid")
        else:
            print("Fell at the first hurdle - package base form is invalid")
            return False

    def save_data(self):
        """
        Retrieve the form data and update an existing package, or create a new package with that data
        :return: the new or edited package
        """
        # HTML checkbox returns "ON" or nothing at all in dict [CHROME] so cannot be passed directly to boolean field
        if 'comments_enabled' in self.package_base_form.cleaned_data \
                and self.package_base_form.cleaned_data['comments_enabled'] is not False:
            comments_enabled = True
        else:
            comments_enabled = False

        if int(self.package_id) == self.NEW_PACKAGE_FLAG:  # TODO: better way to do this?
            package = Package(package_name=self.package_base_form.cleaned_data['package_name'],
                              main_color=self.package_base_form.cleaned_data['main_color'],
                              comments_enabled=comments_enabled,
                              owner=self.owner)
            package.save()
        else:
            package = Package.objects.get(pk=self.package_id)
            package.package_name = self.package_base_form.cleaned_data['package_name']
            package.main_color = self.package_base_form.cleaned_data['main_color']
            package.comments_enabled = comments_enabled
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
