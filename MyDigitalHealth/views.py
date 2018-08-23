from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import RegistrationForm, CreateCardPackage, CreateCardGroup, CreateCards, CreateComments
from .models import Package, Category, Card, Comment
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
            data = request.POST
            new_package = Package(package_name=data['package_name'], owner=request.user)
            new_package.save()

            for category_name in data.getlist('category_name'):
                new_category = Category(package_id=new_package, category_name=category_name, category_owner=request.user)
                new_category.save()

            for card_text in data.getlist('card_text'):
                new_card = Card(package_id=new_package, card_text=card_text)
                new_card.save()

            # load the admin-view-all-the-packages page
            return render(
                request,
                'admin.html',
            )
# TODO else throw 404?


def preview_package(request):
    return render(
        request,
        'package_preview.html',
    )


def register(request):
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
        else:
            form = RegistrationForm()
            args = {'form': form}
            return render(
                request,
                'register.html',
                {'form': form}
            )
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(
            request,
            'register.html',
            {'form': form}
        )


def view(request):
    cardPackages = Package.objects.all()
    return render(
        request,
        'view.html',
    )


def package(request):
    card_packages = Package.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'packages_list.html',
        context
    )


def package_list(request, package_id):
    package = Package.objects.get(id__exact=package_id)
    context = {'package': package}
    return render(
        request,
        'package_active.html',
        context
    )


def admin(request):
    owner = request.user
    own_packages = Package.get_packages_by_owner(owner)
    context = {'own_packages': own_packages}
    return render(
        request,
        'admin.html',
        context
    )


def edit(request, package):
    package = Package.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'edit.html',
        context
    )


def comments(request):
    if request.method =='POST':
        form = CreateComments(request.POST, instance=Comment())
        name = request.POST.get('name')
        cardPackage = Package.objects.get(name = name)
        user = request.user
        comment = request.POST.get('comment')
        comments = Comment(card_package = cardPackage, user = user, comment = comment)
        comments.save()
        return render(
            request,
            'index.html',
        )
    else:
        form = CreateCardPackage(instance=Comment())
        args = {'form': form}
        return render(
            request,
            'package_active.html',
            {'form': form}
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


def cardPackages(request):
    cardPackages = Package.objects.all()
    return TemplateResponse(request, views.index, {'cardPackages': cardPackages})


def cardGroups(request):
    cardGroups = Category.objects.all()
    return TemplateResponse(request, views.index, {'cardGroups': cardGroups})


def cardList(request):
    cardList = Card.objects.all()
    return TemplateResponse(request, views.index, {'cardList': cardList})
