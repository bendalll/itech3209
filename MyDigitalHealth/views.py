from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateCardPackage
from .models import Package, Category, Card, UserCardsort
from django.template.response import TemplateResponse
from MyDigitalHealth import views


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
            # TODO: this should really return an "active package" object with the active items - card text and cat names
            # etc in a dict so they can be easily accessed via template code. Somewhere should define "create pack obj"
            data = request.POST
            new_package = Package(package_name=data['package_name'], owner=request.user)
            new_package.save()

            for category_name in data.getlist('category_name'):
                new_category = Category(package=new_package, category_name=category_name)
                new_category.save()

            for card_text in data.getlist('card_text'):
                new_card = Card(package=new_package, card_text=card_text)
                new_card.save()

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


def admin(request):
    """
    View to generate and display the Administration page with a list of the logged-in user's packages that they own
    """
    owner = request.user
    own_packages = Package.get_packages_by_owner(owner)
    context = {'own_packages': own_packages}
    return render(
        request,
        'admin.html',
        context
    )


def view(request):
    all_packages = Package.objects.all()
    context = {'all_packages': all_packages}
    return render(
        request,
        'view.html',
        context,
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
    active_package = Package.objects.get(id__exact=package_id)
    context = {'active_package': active_package}
    return render(
        request,
        'package_active.html',
        context
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


def editPackage(request, package):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Package())
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
                'admin.html',
            )
        else:
            form = CreateCardPackage(instance=Package())
            args = {'form': form}
            return render(
                request,
                'admin.html',
                {'form': form}
            )
    else:
        form = CreateCardPackage(instance=Package())
        args = {'form': form}
        return render(
            request,
            'admin.html',
            {'form': form}
        )


def card_packages(request):
    available_packages = Package.objects.all()
    return TemplateResponse(request, views.index, {'packages': available_packages})


# def cardGroups(request):
#     cardGroups = Category.objects.all()
#     return TemplateResponse(request, views.index, {'cardGroups': cardGroups})


# def cardList(request):
#     cardList = Card.objects.all()
#     return TemplateResponse(request, views.index, {'cardList': cardList})
