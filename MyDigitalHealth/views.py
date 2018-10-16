from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PackageForm
from .models import Package, SortedPackage, Card, SortedGroup


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
            print("Login form was not valid")
            # TODO: Ensure this returns something meaningful to the user
            form = RegistrationForm()
            args = {'form': form}
            return render(
                request,
                'register.html',
                args
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
            # TODO: Ensure this returns something meaningful to the user
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
    packages = Package.objects.all()
    context = {'packages': packages}
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
            packages = Package.objects.all()
            context = {'packages': packages}
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

        package = Package.objects.get(pk=package_id)
        print(package)

        # Edit Existing Sorted_Packages Object if it exists
        if SortedPackage.objects.filter(parent_package=package, user=request.user).exists():
            sorted_package = SortedPackage.objects.get(parent_package=package, user=request.user)
        else:
            sorted_package = SortedPackage(parent_package=package, user=request.user)
            sorted_package.save()

        # Save the comment if one is in the POST.
        if 'comment' in request.POST:
            sorted_package.comment = request.POST['comment']

        # Process the CSV strings for the card groups
        for group in sorted_package.parent_package.get_groups():
            group_text = request.POST['card_ids_for_' + str(group.pk)]

            if SortedGroup.objects.filter(sorted_package=sorted_package, parent_group=group):
                sorted_group = SortedGroup.objects.get(sorted_package=sorted_package, parent_group=group)
                sorted_group.cards.clear()  # Remove all existing Cards in the ManyToMany relationship
            else:
                sorted_group = SortedGroup(sorted_package=sorted_package,
                                           parent_group=group,
                                           title=group.title)
                sorted_group.save()

            # Iterate through each card pk and add it to the ManyToMany relationship.
            for card_id in group_text.split(','):
                if not card_id == '':       # TODO - Deal more gracefully with blank values
                    card = Card.objects.get(pk=card_id)
                    sorted_group.cards.add(card)

        sorted_package.save()

        context = package.to_dict()
        return render(
            request,
            'index.html',
            context
        )
    else:

        if SortedPackage.objects.filter(parent_package=package_id, user=request.user).exists():
            package = SortedPackage.objects.get(parent_package=package_id, user=request.user)

        else:
            package = Package.objects.get(pk=package_id)

        context = package.to_dict()
        return render(
            request,
            'activity.html',
            context
        )


def delete_package(request, package_id):
    """ Remove the package from the database """
    # TODO: put this in a try/catch for db errors
    package = Package.objects.get(pk=package_id)
    package.delete()
    # TODO: return some indicator of success or failure
    packages = Package.objects.all()
    context = {'packages': packages}
    return render(
        request,
        'administration.html',
        context
    )


def get_css(request, package_id):
    """ Return the css with the correct heading color for the package """
    package = Package.objects.get(pk=package_id)
    main_color = package.main_color
    return render(
        request,
        'heading_colors.css',
        {'main_color': main_color},
        content_type='text/css'
    )
