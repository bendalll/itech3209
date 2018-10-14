from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PackageForm
from .models import Card_Packages


def index(request):
    """ View function for home page of site """
    return render(
        request,
        'index.html',
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
            args
        )


def create_package(request):
    if request.method == 'POST':
        form = PackageForm(request=request)
        if form.is_valid():
            form.save_data()
            return render(
                request,
                'index.html',
            )
        else:
            print("Form failed validation: ", form.errors)
            form = PackageForm()
            context = form.to_dict()
            return render(
                request,
                'create_edit_package.html',
                context
            )
    else:
        form = PackageForm()
        context = form.to_dict()
        return render(
            request,
            'create_edit_package.html',
            context
        )


def package_administration(request):
    card_packages = Card_Packages.objects.all()
    context = {'card_packages': card_packages}
    return render(
        request,
        'administration.html',
        context
    )


def edit_package(request, package_id):
    if request.method == 'POST':
        form = PackageForm(request=request)
        if form.is_valid():
            form.save_data()
            card_packages = Card_Packages.objects.all()
            context = {'card_packages': card_packages}
            return render(
                request,
                'administration.html',
                context
            )
        else:
            print("Form data is invalid:", form.errors)
            return redirect(
                request.path_info
            )
    else:
        form = PackageForm(package_id=package_id)
        context = form.to_dict()
        return render(
            request,
            'create_edit_package.html',
            context
        )


def cardsort_activity(request, package_id):
    if request.method == 'POST':
        # TODO: THIS
        print(request.POST)
        package = Card_Packages.objects.get(pk=package_id)
        context = package.to_dict()
        return render(
            request,
            'index.html',
            context
        )
    else:
        package = Card_Packages.objects.get(pk=package_id)
        context = package.to_dict()
        return render(
            request,
            'activity.html',
            context
        )


def delete_package(request, package_id):
    """ Remove the package from the database """
    # TODO: put this in a try/catch for db errors
    package = Card_Packages.objects.get(pk=package_id)
    package.delete()
    # TODO: return some indicator of success or failure
    card_packages = Card_Packages.objects.all()
    context = {'card_packages': card_packages}
    return render(
        request,
        'administration.html',
        context
    )


def get_css(request, package_id):
    """ Return the css with the correct heading color for the package """
    package = Card_Packages.objects.get(pk=package_id)
    main_color = package.main_color
    return render(
        request,
        'heading_colors.css',
        {'main_color': main_color},
        content_type='text/css'
    )
