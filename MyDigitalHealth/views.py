from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import RegistrationForm, create_blank_form, validate_and_create_package, edit_package_form
from .models import Package, Category, Card, UserCardsort
from .context_processors import admin_own_packages


def index(request):
    """
    View function for home page of site.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},  # num_visits appended
    )


def register(request):
    """
    View to create a new user with data provided
    **Fails if the password does not meet the requirements, without advising the user of the reason**
    If successful, creates the user, logs them in and sends to home page;
    If fails, refreshes the page with no additional information currently
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(
                request,
                'index.html',
            )
        else:  # TODO meaningful "else" functionality
            form = RegistrationForm()
            args = {'form': form}
            return render(
                request,
                'register.html',
                {'form': form}
            )
    else:  # TODO meaningful "else" functionality
        form = RegistrationForm()
        args = {'form': form}
        return render(
            request,
            'register.html',
            {'form': form}
        )


def create_package(request):
    """
        Administrator functionality to create new Packages with related Cards and Categories
    """
    if request.method == 'POST':
        print(request.POST)
        #  new_package = validate_and_create_package(request)
        return HttpResponseRedirect('admin')

    else:
        form = create_blank_form()

        return render(
            request,
            'create_package.html',
            context=form
        )


def package_preview(request, package_id):
    """
    Generate a preview of a package to allow the Administrator to see it as the user would see it

    TODO change name to 'load_cards' and extend template for admin vs user view
    TODO: nope that's bad, move functionality further back to models and make it modular
    """
    active_package = Package.get_package_by_id(package_id)
    card_list = Card.objects.filter(package=active_package)
    category_list = Category.objects.filter(package=active_package)
    # Pass through as accessible lists as context for ease of processing
    context = {'active_package': active_package,
               'card_list': card_list,
               'category_list': category_list
               }
    if request.user.is_staff:
        return render(
            request,
            'package_preview.html',
            context
        )
    else:
        return render(
            request,
            'package_preview.html',
            context
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def package_administration(request):
    """
    View to generate and display the Administration page with a list of the packages the admin has created
    """
    own_packages = admin_own_packages(request)
    context = {'own_packages': own_packages}
    return render(
        request,
        'package_administration.html',
        context
    )


def package(request):
    all_packages = Package.objects.all()
    context = {'all_packages': all_packages}
    return render(
        request,
        'packages_dropdown_list.html',
        context
    )


def open_package(request, package_id):
    """
    Take a package id and generate the activity page for the user to card sort with that package
    """
    active_package = Package.get_package_by_id(package_id)
    card_list = Card.objects.filter(package=active_package)
    category_list = Category.objects.filter(package=active_package)
    # Pass through as accessible lists as context for ease of processing
    context = {'active_package': active_package,
               'card_list': card_list,
               'category_list': category_list
               }
    return render(
        request,
        'package_active.html',
        context
    )


def save(request, package_id):
    return(
        request,
        'index.html'
    )


def edit_package(request, package_id):
    filled_form = edit_package_form(package_id)
    return render(
        request,
        'create_package.html',
        context=filled_form
    )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def edit_save(request, package_id):
    if request.method == 'POST':
        if validate_input(request):
            data = request.POST
            active_package = Package.objects.get(pk=package_id)
            cat_ids = data.getlist('category_id')
            cat_names = data.getlist('cur_category_name')
            for category_id, category_name in zip(cat_ids, cat_names):
                category = Category.objects.get(pk=category_id)
                category.category_name = category_name
                category.save()

            card_ids = data.getlist('card_id')
            card_texts = data.getlist('cur_card_text')
            for card_id, card_text in zip(card_ids, card_texts):
                card = Card.objects.get(pk=card_id)
                card.card_text = card_text
                card.save()

            # TODO: tidy this code
            # if Categories or Cards were removed, delete them
            # get the list of ids as the package thinks they are
            cur_categorylist = Category.objects.filter(package=active_package)
            # turn the list into a list of ints for ease of comparison
            int_cat_ids = []
            for cat_id in cat_ids:
                int_id = int(cat_id)
                int_cat_ids.append(int_id)

            # compare the lists and remove the Categories that have been edited out by the admin
            for category in cur_categorylist:
                if category.pk not in int_cat_ids:
                    category.delete()

            # repeat for Cards
            cur_cardlist = Card.objects.filter(package=active_package)
            # turn the list into a list of ints for ease of comparison
            int_card_ids = []
            for card_id in card_ids:
                int_id = int(card_id)
                int_card_ids.append(int_id)

            # compare the lists and remove the Categories that have been edited out by the admin
            for card in cur_cardlist:
                if card.pk not in int_card_ids:
                    card.delete()

            # if new Categories or Cards were added, create them
            new_categories = data.getlist('category_name')
            for category_name in new_categories:
                new_category = Category(category_name=category_name, package=active_package)
                new_category.save()

            new_cards = data.getlist('card_text')
            for card_text in new_cards:
                new_card = Card(card_text=card_text, package=active_package)
                new_card.save()

            # TODO: success message and redirect
            return redirect('admin')
        else:
            messages.info(request, 'Something went wrong. Please ensure all fields are filled out.')
            return redirect('edit_package')
    else:
        messages.info(request, 'Something went wrong. Sorry!')
        return redirect('edit_package')


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_choose_user(request, package_id):
    active_package = Package.objects.get(pk=package_id)
    user_list = User.objects.all()
    context = {'active_package': active_package,
               'user_list': user_list
               }
    return render(
        request,
        'assign_package.html',
        context
    )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_package_to_user(request, package_id, user_id):
    """
    Function to assign the activate package to the provided user - creates instance of UserCardsort
    """
    # get the package by id
    active_package = Package.objects.get(pk=package_id)
    # get the user by id
    assigned_user = User.objects.get(pk=user_id)
    # check if UserCardsort already exists
    all_pack_assignments = UserCardsort.objects.all()
    for cardsort in all_pack_assignments:
        # if exists, return and say already assigned
        # TODO: change this so that you can tell it's already assigned on the page, and don't have to make this call
        if cardsort.package == active_package and cardsort.user == assigned_user:
            context = {'message': "This package is already assigned to this user"}
            return render(
                request,
                'assign_package.html',
                context
            )
        # if not exist, create it and provide success message
        else:
            assignment = UserCardsort(package=active_package, user=assigned_user)
            assignment.save()
            context = {'assignment': assignment}
            return render(
                request,
                'assign_package.html',
                context
            )
    # Nothing exists there yet so have to make the first item and then this code won't be used
    else:
        assignment = UserCardsort(package=active_package, user=assigned_user)
        assignment.save()
        context = {'assignment': assignment}
        return render(
            request,
            'assign_package.html',
            context
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def delete_package(request, package_id):
        to_delete = Package.objects.get(pk=package_id)
        # TODO: try/catch delete errors here
        to_delete.delete()
        print("So it printed... above...")
        context = {'message': "Delete successful"}
        # TODO: redirect this to the same page with success/fail context
        return render(
            request,
            'assign_package.html',
            context
        )


"""
Code that I don't know if it is used-->
"""


def card_packages(request):
    available_packages = Package.objects.all()
    return TemplateResponse(request, 'index.html', {'packages': available_packages})


# def cardGroups(request):
#     cardGroups = Category.objects.all()
#     return TemplateResponse(request, views.index, {'cardGroups': cardGroups})


# def cardList(request):
#     cardList = Card.objects.all()
#     return TemplateResponse(request, views.index, {'cardList': cardList})

"""
def view(request):
    all_packages = Package.objects.all()
    context = {'all_packages': all_packages}
    return render(
        request,
        'view.html',
        context,
    )


def comments(request):
    if request.method == 'POST':
        # TODO get the comments from the form and save them to UserCardsort item
        return render(
            request,
            'index.html',
        )
    else:
        # TODO something meaningful here
        return render(
            request,
            'index.html'
        )


def edit(request, package_in):
    active_package = Package.objects.filter(package=package_in)
    context = {'active_package': active_package}
    return render(
        request,
        'edit.html',
        context
    )
"""


# TODO: Move this to a different place but code is here for now
# Function to get the cards to populate the dropdown list
def get_cards_for_dropdown(request):
    user = request.user
    # TODO: create package/user relationship


# TODO: remove this and refactor code accordingly
def validate_input(request):
    """
    Function to ensure input from create or edit card page is not blank
    TODO: improve this, possibly using Form validation instead
    """
    data = request.POST
    categorylist = data.getlist('category_name')
    cardlist = data.getlist('card_text')

    if data['package_name'] != "":
        for name in categorylist:
            if name != "":
                pass
            else:
                return False  # messages.info(request, 'A category name provided is invalid.')
        for text in cardlist:
            if text != "":
                pass
            else:
                return False  # messages.info(request, "A card text value provided is invalid.")
        # if we made it to here, everything is valid and return True
        return True
    else:
        return False  # messages.info(request, 'The package name provided is invalid.')