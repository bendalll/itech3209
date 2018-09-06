from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import RegistrationForm, create_blank_form, validate_and_create_package, edit_package_form, \
    get_whole_package
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
        new_package = validate_and_create_package(request)
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

    #TODO this is a duplicate of open_package
    """
    context = get_whole_package(package_id)
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

    # TODO this is a duplicate of open_package
    """
    context = get_whole_package(package_id)
    if request.user.is_staff:
        return render(
            request,
            'package_active.html',
            context
        )
    else:  # TODO: this else makes no sense
        return render(
            request,
            'package_active.html',
            context
        )


def save(request, package_id):
    # TODO: this should create a UserCardsort object with the positions of cards in categories from request.POST
    if request.method == "POST":
        data = request.POST
        package = Package.objects.get(pk=package_id)
        cards_unassigned = data['card_ids_unassigned'].split(',')
        sortlist = {}

        # Check if save thing exists
        if UserCardsort.objects.filter(package=package, user=request.user).exists():
            UserCardsort.objects.get(package=package, user=request.user).delete()

        print(package.get_package_categories())

        for category in package.get_package_categories():
            new_sortlist = data['card_ids_for_' + str(category.pk)].split(',')
            for card in new_sortlist:
                sortlist[card] = category.pk

            print(sortlist)
    return redirect('open_package', package_id)


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
        # Just delete the current package and create it all again
        Package.objects.get(pk=package_id).delete()
        new_package = validate_and_create_package(request)
        return redirect('admin')

    else:
        messages.info(request, 'Something went wrong. Please ensure all fields are filled out.')
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
    Function to assign the active package to the provided user - creates instance of UserCardsort
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
        instance = Package.objects.get(pk=package_id)
        # TODO: try/catch delete errors here
        instance.delete()
        own_packages = admin_own_packages(request)
        context = {'own_packages': own_packages, 'message': 'Delete successful'}
        return render(
            request,
            'package_administration.html',
            context
        )


"""
Code that I don't know if it is used-->
"""


def card_packages(request):
    available_packages = Package.objects.all()
    return TemplateResponse(request, 'index.html', {'packages': available_packages})


# TODO: Move this to a different place but code is here for now
# Function to get the cards to populate the dropdown list
def get_cards_for_dropdown(request):
    user = request.user
    # TODO: create package/user relationship
