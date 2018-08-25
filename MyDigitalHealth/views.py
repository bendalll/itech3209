from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegistrationForm, CreatePackage, CreateCategory, CreateCard
from .models import Package, Category, Card, UserCardsort
from .context_processors import get_admin_own_packages


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
    If request is GET, displays the form to enter data for new Package
    If request is POST, should submit data and create new Package, then redirect to Package list
    """
    if request.method == 'GET':
        return render(
            request,
            'create_package.html',
        )
    else:
        if request.method == 'POST':
            # get data from request.POST and create cards and categories and new package as objects
            # save new objects to the database
            # etc in a dict so they can be easily accessed via template code. Somewhere should define "create pack obj"
            data = request.POST
            package_form = CreatePackage(data, instance=Package())
            category_form = CreateCategory(data, instance=Category())
            card_form = CreateCard(data, instance=Card())

            if package_form.is_valid() and category_form.is_valid() and card_form.is_valid():
                new_package_name = package_form.cleaned_data.get('package_name')
                new_package = Package(package_name=new_package_name, owner=request.user)
                # new_package.save()

                category_name = category_form.cleaned_data.get('category_name')
                print(category_name)

            else:
                print("We got here but [a value] provided was invalid")
                # raise a validation error
                # return the error message to the user e.g. "Package Name invalid"

            # for category_name in data.getlist('category_name'):
            #     new_category = Category(package=new_package, category_name=category_name)
            #     new_category.save()
            #
            # for card_text in data.getlist('card_text'):
            #     new_card = Card(package=new_package, card_text=card_text)
            #     new_card.save()

            return redirect('admin')
# TODO else do something useful


def package_preview(request, package_id):
    """
    Generate a preview of a package to allow the Administrator to see it as the user would see it

    TODO change name to 'load_cards' and extend template for admin vs user view
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
    own_packages = get_admin_own_packages(request)
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
    active_package = Package.objects.get(pk=package_id)
    context = {'active_package': active_package}
    return render(
        request,
        'package_active.html',
        context
    )


def edit_package(request, package_id):
    active_package = Package.objects.get(pk=package_id)
    cardlist = Card.objects.filter(package_id=active_package.pk)
    categorylist = Category.objects.filter(package_id=active_package.pk)
    context = {'active_package': active_package,
               'cardlist': cardlist,
               'categorylist': categorylist
               }
    return render(
        request,
        'edit_package.html',
        context
    )


def edit_package_OLD(request, package_id):
    if request.method == 'POST':
        form = CreatePackage(request.POST, instance=Package())
        if form.is_valid():
            cardPackage = Package.objects.get(id__exact=package)
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            cardGroupIDs = request.POST.getlist('cardGroupID')
            cardListIDs = request.POST.getlist('cardListID')
            name = request.POST.get('name')
            user = request.user
            cardPackage.name = name
            cardPackage.save()
            group = Category()
            card = Card()
            for cardGroupID, title in zip(cardGroupIDs, titles):
                group.id = cardGroupID
                group.card_package = cardPackage
                group.title = title
                group.save()
            for cardListID, text in zip(cardListIDs, texts):
                card.id = cardListID
                card.card_package = cardPackage
                card.card_group = group
                card.text = text
                card.save()
            return render(
                request,
                'package_administration.html',
            )
        else:
            form = CreatePackage(instance=Package())
            args = {'form': form}
            return render(
                request,
                'package_administration.html',
                {'form': form}
            )
    else:
        form = CreatePackage(instance=Package())
        args = {'form': form}
        return render(
            request,
            'package_administration.html',
            {'form': form}
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def edit_save(request, package_id):
    if request.method == 'POST':
        package_form = CreatePackage(request.POST, instance=Package())

        if package_form.is_valid():
            active_package = Package.objects.get(pk=package_id)
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            cardGroupIDs = request.POST.getlist('cardGroupID')
            cardListIDs = request.POST.getlist('cardListID')
            name = request.POST.get('name')
            user = request.user
            cardPackage.name = name
            cardPackage.save()
            group = Category()
            card = Card()
            for cardGroupID, title in zip(cardGroupIDs, titles):
                group.id = cardGroupID
                group.card_package = cardPackage
                group.title = title
                group.save()
            for cardListID, text in zip(cardListIDs, texts):
                card.id = cardListID
                card.card_package = cardPackage
                card.card_group = group
                card.text = text
                card.save()
            return render(
                request,
                'package_administration.html',
            )
    return render(
        request,
        'package_administration.html'
    )


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