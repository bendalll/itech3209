from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateCardPackage, CreateCardGroup, CreateCards
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Card_Packages, Card_Groups, Cards
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
		context={'num_visits':num_visits}, # num_visits appended
    )
	
def create(request):
    return render(
        request,
        'project.html',
    )
	
def getCards(request):
    cards = Cards.objects.all() 
    return TemplateResponse(request, views.index, {'cards': cards})
	
def cards(request):
    if request.method =='POST':
        form = CreateCardPackage(request.POST, instance=Card_Packages())
        if form.is_valid():
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            names = request.POST.getlist('name')
            for name in names:
                cardPackage = Card_Packages(name = name)
                cardPackage.save()
            for title in titles:
                group = Card_Groups(card_package = cardPackage, title = title)
                group.save()
            for text in texts:
                card = Cards(card_package = cardPackage, text = text)
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
    if request.method =='POST':
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
	
def cardPackages(request):
    cardPackages = Card_Packages.objects.all() 
    return TemplateResponse(request, views.index, {'cardPackages': cardPackages})
	
def cardGroups(request):
    cardGroups = Card_Groups.objects.all() 
    return TemplateResponse(request, views.index, {'cardGroups': cardGroups})

def cardList(request):
    cardList = Cards.objects.all() 
    return TemplateResponse(request, views.index, {'cardList': cardList})
	
def cardPackagesView(request,id):
   cardPackages = Card_Packages.objects.get(id=id) 
   return render(request, 'index.html')