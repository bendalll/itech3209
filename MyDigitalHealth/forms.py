from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, modelformset_factory, CheckboxInput

from .models import Card_Packages, Card_Groups, Cards


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


class PackageBaseForm(forms.ModelForm):
    class Meta:
        model = Card_Packages
        fields = (
            'name',
            'main_color',
            'comments_allowed',
            'user_defined_groups'
        )
        labels = {
            'name': 'Name of Card Package',
            'main_color': 'Colour of Group Headings',
            'user_defined_groups': 'Let User Name the Groups'
        }
        widgets = {
            'main_color': TextInput(attrs={'type': 'color', 'onchange': 'changeHeadingColor()'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'user_defined_groups': CheckboxInput(attrs={'onchange': 'toggleGroupsInput()'})
        }


def create_groups_formset(**kwargs):
    """ Function to create and return a model formset of Group Forms """

    widgets = {'title': TextInput(attrs={'class': 'form-control'})}
    labels = {'title': ''}

    # Filter for 'extra' here to avoid always having to specify extra=0
    if 'extra' in kwargs:
        GroupsFormset = modelformset_factory(
            Card_Groups,
            fields=('title',),
            labels=labels,
            widgets=widgets,
            extra=kwargs['extra']
        )
    else:
        GroupsFormset = modelformset_factory(
            Card_Groups,
            fields=('title',),
            labels=labels,
            widgets=widgets,
            extra=0
        )

    if 'package' in kwargs:
        new_category_formset = GroupsFormset(queryset=Card_Groups.objects.filter(card_package=kwargs['package']),
                                             prefix='group')
    elif 'request' in kwargs:
        new_category_formset = GroupsFormset(kwargs['request'].POST, kwargs['request'].FILES, prefix='group')
    else:
        new_category_formset = GroupsFormset(queryset=Card_Groups.objects.none(), prefix='group')

    for form in new_category_formset:
        form.empty_permitted = False

    return new_category_formset


def create_cards_formset(**kwargs):
    """ Function to create and return and model formset of Card Forms """
    widgets = {'text': TextInput(attrs={'class': 'form-control'})}
    labels = {'text': ''}

    # Filter for 'extra' here to avoid always having to specify extra=0
    if 'extra' in kwargs:
        CardsFormset = modelformset_factory(
            Cards,
            fields=('text',),
            labels=labels,
            widgets=widgets,
            extra=kwargs['extra']
        )
    else:
        CardsFormset = modelformset_factory(
            Cards,
            fields=('text',),
            labels=labels,
            widgets=widgets,
            extra=0
        )

    if 'package' in kwargs:
        new_card_formset = CardsFormset(queryset=Cards.objects.filter(card_package=kwargs['package']), prefix='card')
    elif 'request' in kwargs:
        new_card_formset = CardsFormset(kwargs['request'].POST, kwargs['request'].FILES, prefix='card')
    else:
        new_card_formset = CardsFormset(queryset=Cards.objects.none(), prefix='card')

    for form in new_card_formset:
        form.empty_permitted = False

    return new_card_formset


class PackageForm(forms.Form):
    """ Class to create a blank form for making a package, and create a new package object when submitted """
    NEW_PACKAGE_FLAG = -1
    num_groups = 2  # default the number of group name input fields to this
    num_cards = 4  # default the number of card text input fields to this

    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'request' in kwargs:
            """ Checks whether the form is being created with POST data, and so populates it with that data in
            preparation for validation """
            request = kwargs['request']

            # Create a form with the POST data, to be validated

            if 'comments_allowed' in request.POST:  # checkbox value does not come in as true/false
                comments_allowed = True
            else:
                comments_allowed = False

            if 'user_defined_groups' in request.POST: # checkbox value does not come in as true/false
                user_defined_groups = True
            else:
                user_defined_groups = False

            self.package_base_form = PackageBaseForm({'name': request.POST['name'],
                                                      'main_color': request.POST['main_color'],
                                                      'comments_allowed': comments_allowed,
                                                      'user_defined_groups': user_defined_groups})
            self.groups_formset = create_groups_formset(request=request)
            self.cards_formset = create_cards_formset(request=request)
            self.user = request.user
            self.package_id = request.POST['package_id']

        elif 'package_id' in kwargs and kwargs['package_id'] != -1:
            """ Checks whether the form is being created to edit a given package, and so populates it with the package
            information so it can be edited """
            package = Card_Packages.objects.get(pk=kwargs['package_id'])
            self.package_base_form = PackageBaseForm(instance=package)
            self.groups_formset = create_groups_formset(package=package)
            self.cards_formset = create_cards_formset(package=package)
            self.package_id = kwargs['package_id']
        else:
            """ Default to create a new, blank form, with the default number of group and card inputs, to create a
            new package """
            self.package_base_form = PackageBaseForm()
            if 'num_groups' in kwargs:
                self.num_groups = kwargs['num_groups']
            if 'num_cards' in kwargs:
                self.num_cards = kwargs['num_cards']

            self.groups_formset = create_groups_formset(extra=self.num_groups)
            self.cards_formset = create_cards_formset(extra=self.num_cards)
            self.package_id = self.NEW_PACKAGE_FLAG

    def __str__(self):
        return "Form to create, edit, or submit a package or package information"

    def to_dict(self):
        """ Get the Form as a dict that is easy to pass through as context for template to render """
        package = {'package_base_form': self.package_base_form,
                   'groups_formset': self.groups_formset,
                   'cards_formset': self.cards_formset,
                   'package_id': self.package_id}
        return package

    def is_valid(self):
        """ Validate each of the included forms/formsets in the collected form object """
        if self.package_base_form.is_valid():
            if self.groups_formset.is_valid():
                if self.cards_formset.is_valid():
                    return True
                else:
                    print("Cards formset is invalid")
            else:
                print("Groups formset is invalid")
        else:
            print("Fell at the first hurdle - package base form is invalid")
            return False

    def save_data(self):
        """
        Retrieve the form data and update an existing package, or create a new package with that data
        :return: the new or edited package
        """
        # HTML checkbox returns "ON" or nothing at all in dict [CHROME] so cannot be passed directly to boolean field
        if 'comments_allowed' in self.package_base_form.cleaned_data \
                and self.package_base_form.cleaned_data['comments_allowed'] is not False:
            comments_allowed = True
        else:
            comments_allowed = False
        # HTML checkbox returns "ON" or nothing at all in dict [CHROME] so cannot be passed directly to boolean field
        if 'user_defined_groups' in self.package_base_form.cleaned_data \
                and self.package_base_form.cleaned_data['user_defined_groups'] is not False:
            user_defined_groups = True
        else:
            user_defined_groups = False

        if int(self.package_id) == self.NEW_PACKAGE_FLAG:  # TODO: better way to do this?
            package = Card_Packages(name=self.package_base_form.cleaned_data['name'],
                                    owner=self.user,
                                    main_color=self.package_base_form.cleaned_data['main_color'],
                                    comments_allowed=comments_allowed,
                                    user_defined_groups=user_defined_groups)
            package.save()
        else:
            package = Card_Packages.objects.get(pk=self.package_id)
            package.name = self.package_base_form.cleaned_data['name']
            package.main_color = self.package_base_form.cleaned_data['main_color']
            package.comments_allowed = comments_allowed
            package.user_defined_groups = user_defined_groups
            package.save()

            # easiest to delete all the existing data and create it again
            for group in package.get_groups():
                group.delete()
            for card in package.get_cards():
                card.delete()

        print(self.groups_formset.cleaned_data)
        print(self.cards_formset.cleaned_data)
        for group in self.groups_formset.cleaned_data:
            title = group['title']
            new_group = Card_Groups(title=title, card_package=package)
            new_group.save()

        for card in self.cards_formset.cleaned_data:
            text = card['text']
            new_card = Cards(text=text, card_package=package)
            new_card.save()

        return package
