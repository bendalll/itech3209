from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateCardPackage, CreateCardGroup, CreateCards, CreateComments
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Card_Packages, Card_Groups, Cards, Comments
from django.template.response import TemplateResponse
from django.contrib import messages 


def index(request):
    """
    View function for home page of site.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},  # num_visits appended
    )


def create(request):
    return render(
        request,
        'project.html',
    )


def cards(request):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Card_Packages())
        if form.is_valid():
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            groups = request.POST.getlist('group')
            names = request.POST.getlist('name')
            user = request.user
            for name in names:
                cardPackage = Card_Packages(name=name, user=user)
                cardPackage.save()
            for title in titles:
                group = Card_Groups(card_package=cardPackage, title=title)
                group.save()
            for text in texts:
                card = Cards(card_package=cardPackage, card_group=group, text=text)
                card.save()
            return render(
                request,
                'index.html',
            )
        else:
            form = CreateCardPackage(instance=Card_Packages())
            args = {'form': form}
            return render(
                request,
                'project.html',
                {'form': form}
            )
    else:
        form = CreateCardPackage(instance=Card_Packages())
        args = {'form': form}
        return render(
            request,
            'project.html',
            {'form': form}
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
    cardPackages = Card_Packages.objects.all()
    return render(
        request,
        'view.html',
    )


def package(request):
    cardPackages = Card_Packages.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'package.html',
        context
    )


def packageList(request, package):
    package = Card_Packages.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'packageList.html',
        context
    )


def admin(request):
    cardPackages = Card_Packages.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'admin.html',
        context
    )


def edit(request, package):
    package = Card_Packages.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'edit.html',
        context
    )


def comments(request):
    if request.method =='POST':
        form = CreateComments(request.POST, instance=Comments())
        name = request.POST.get('name')
        cardPackage = Card_Packages.objects.get(name = name)
        user = request.user
        comment = request.POST.get('comment')
        comments = Comments(card_package = cardPackage, user = user, comment = comment)
        comments.save()
        return render(
            request,
            'index.html',
        )
    else:
        form = CreateCardPackage(instance=Comments())
        args = {'form': form}
        return render(
            request,
            'packageList.html',
            {'form': form}
        )


def editPackage(request, package):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Card_Packages())
        if form.is_valid():
            cardPackage = Card_Packages.objects.get(id__exact=package)
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            cardGroupIDs = request.POST.getlist('cardGroupID')
            cardListIDs = request.POST.getlist('cardListID')
            name = request.POST.get('name')
            user = request.user
            cardPackage.name = name
            cardPackage.save()
            group = Card_Groups()
            card = Cards()
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
            form = CreateCardPackage(instance=Card_Packages())
            args = {'form': form}
            return render(
                request,
                'admin.html',
                {'form': form}
            )
    else:
        form = CreateCardPackage(instance=Card_Packages())
        args = {'form': form}
        return render(
            request,
            'admin.html',
            {'form': form}
        )


def deletePackage(request, package_id):
    """ Remove the package (as provided by package id) from the database """
    # TODO: put this in a try/catch for db errors
    package = Card_Packages.objects.get(pk=package_id)
    package.delete()
    # TODO: return some indicator of success or failure other than rendering the page again without that package
    cardPackages = Card_Packages.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'admin.html',
        context
    )


def cardPackages(request):
    cardPackages = Card_Packages.objects.all() 
    return TemplateResponse(request, views.index, {'cardPackages': cardPackages})


def cardGroups(request):
    cardGroups = Card_Groups.objects.all() 
    return TemplateResponse(request, views.index, {'cardGroups': cardGroups})


def cardList(request):
    cardList = Cards.objects.all() 
    return TemplateResponse(request, views.index, {'cardList': cardList})
