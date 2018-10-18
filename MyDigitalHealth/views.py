from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PackageForm
from .models import Package, SortedPackage, Card, SortedGroup, Permission
from django.db.utils import DatabaseError, IntegrityError, DataError


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

            formErrors = form.errors #assign the form errors or they will be overwritten with the new form.
            messages.error(request,"Please fill out all the required fields correctly.")
            form = RegistrationForm()
            args = {'form': form, 'errormessage': formErrors}
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
            messages.success(request, "Package created Successfully.")
            return render(
                request,
                'index.html',
            )
        else:
            print("INFO: Form failed validation: ", form.errors)
            messages.error(request, "Error Saving. Please ensure you have filled out all of the required fields.")
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
    packages = Package.objects.filter(owner=request.user)
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
            packages = Package.objects.filter(owner=request.user)
            context = {'packages': packages}
            messages.success(request, "Package changes saved.")
            return render(
                request,
                'administration.html',
                context
            )
        else:
            print("INFO: Form data is invalid:", form.errors)
            messages.error(request, "Error Saving. Please ensure you have filled out all of the required fields.")
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
        # Edit Existing Sorted_Packages Object if it exists
        if SortedPackage.objects.filter(parent_package=package, user=request.user).exists():
            sorted_package = SortedPackage.objects.get(parent_package=package, user=request.user)
        else:
            sorted_package = SortedPackage(parent_package=package, user=request.user)
            sorted_package.save()

        # Process the CSV strings for the card groups
        for group in sorted_package.parent_package.get_groups():

            if SortedGroup.objects.filter(sorted_package=sorted_package, parent_group=group):
                sorted_group = SortedGroup.objects.get(sorted_package=sorted_package, parent_group=group)
                sorted_group.cards.clear()  # Remove all existing Cards in the ManyToMany relationship
                group_text = request.POST['card_ids_for_' + str(sorted_group.pk)]
            else:
                group_text = request.POST['card_ids_for_' + str(group.pk)]
                sorted_group = SortedGroup(sorted_package=sorted_package,
                                           parent_group=group,
                                           title=group.title)
                sorted_group.save()

            # Iterate through each card pk and add it to the ManyToMany relationship.
            for card_id in group_text.split(','):
                if not card_id == '':       # TODO - Deal more gracefully with blank values
                    card = Card.objects.get(pk=card_id)
                    sorted_group.cards.add(card)

        # Save the comment if one is in the POST.
        if 'comment' in request.POST:
            sorted_package.comment = request.POST['comment']

        sorted_package.save()
        messages.success(request, "Changes to "+package.name+" Saved.")
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
    try:
        package = Package.objects.get(pk=package_id)
        tempname = package.name
        package.delete()
        messages.success(request, "Package \'"+tempname+"\' deleted Successfully.")
    except KeyError:
        messages.error(request, "Sorry, something went wrong and we couldn't find that package to delete it")
    except DatabaseError as e:
        messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
                       + e.__cause__ )
        print("ERROR: Database Error Deleting Package #" + package.id + "\n\r" + e.__cause__ )
    except DataError as e:
        messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
                       + e.__cause__)
        print("ERROR: Data Error Deleting Package #" + package.id + "\n\r" + e.__cause__)
    except IntegrityError as e:
        messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
                       + e.__cause__ )
        print("ERROR: Integrity Error Deleting Package #" + package.id + "\n\r" + e.__cause__)

    packages = Package.objects.filter(owner=request.user)
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


def get_assigned_packages(request):
    """ Return a list of packages that have been assigned to the logged-in user """
    # filter the permissions to retrieve the permitted packages
    permissions = Permission.objects.filter(user=request.user)
    packages = []
    for permission in permissions:
        permitted_package = Package.objects.get(id=permission.package_id)
        packages.append(permitted_package)
    print(packages)
