from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PackageForm
from .models import Package, SortedPackage, Card, SortedGroup, Permission
# from django.db.utils import DatabaseError, IntegrityError, DataError


def index(request):
    """ View function for home page of site """
    return render(
        request,
        'index.html',
    )


def register(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            password = registration_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(
                request,
                'index.html',
            )
        else:

            form_errors = registration_form.errors  # assign the form errors or they will be overwritten with new form
            messages.error(request, "Please fill out all the required fields correctly.")
            registration_form = RegistrationForm()
            args = {'form': registration_form, 'errormessage': form_errors}
            return render(
                request,
                'register.html',
                args
            )
    else:
        registration_form = RegistrationForm()
        args = {'form': registration_form}
        return render(
            request,
            'register.html',
            args
        )


def create_package(request):
    """ Render the page to create a new package; process the POST data from the page to create a new package """
    if request.method == 'POST':
        package_form = PackageForm(request=request)
        if package_form.is_valid():
            package_form.save_data()
            messages.success(request, "Package created successfully")
            return render(
                request,
                'index.html',
            )
        else:
            print("INFO: Form failed validation: ", package_form.errors)
            messages.error(request, "Error Saving. Please ensure you have filled out all of the required fields.")
            context = package_form.to_dict()
            return render(
                request,
                'create_edit_package.html',
                context
            )
    else:
        package_form = PackageForm()
        context = package_form.to_dict()
        return render(
            request,
            'create_edit_package.html',
            context
        )


def package_administration(request):
    own_packages = _admin_get_own_packages(request)
    context = {'own_packages': own_packages}
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
            own_packages = _admin_get_own_packages(request)
            package_name = Package.objects.get(id=package_id).name
            context = {'own_packages': own_packages}
            messages.success(request, "Changes to "+package_name+" saved. All sorted cards have been reset.")
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


def package_permissions(request, package_id):
    package = Package.objects.get(pk=package_id)
    users = User.objects.all()
    for user in users:
        if Permission.objects.filter(package=package, user=user):
            user.has_permission = True
    context = {'users': users, 'package': package}
    return render(
        request,
        'package_permissions.html',
        context
    )


def assign_package(request, package_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['user_id'])
        package = Package.objects.get(pk=package_id)
        if Permission.objects.filter(package=package, user=user).exists():
            messages.error(request, "Package is already assigned to this user")
            users = User.objects.all()
            for user in users:
                if Permission.objects.filter(package=package, user=user):
                    user.has_permission = True
            context = {'users': users, 'package': package}
            return render(
                request,
                'package_permissions.html',
                context
            )
        else:
            assignment = Permission(package=package, user=user)
            assignment.save()
            package = Package.objects.get(pk=package_id)
            users = User.objects.all()
            for user in users:
                if Permission.objects.filter(package=package, user=user):
                    user.has_permission = True
            context = {'users': users, 'package': package}
            return render(
                request,
                'package_permissions.html',
                context
            )
    else:
        package = Package.objects.get(pk=package_id)
        users = User.objects.all()
        for user in users:
            if Permission.objects.filter(package=package, user=user):
                user.has_permission = True
        context = {'users': users, 'package': package}
        return render(
            request,
            'package_permissions.html',
            context
        )


def unassign_package(request, package_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['user_id'])
        package = Package.objects.get(pk=package_id)
        try:
            permission = Permission.objects.get(package=package, user=user)
            permission.delete()
        except KeyError:
            messages.error(request, "Unable to unassign package from this user")
            print("Well that didn't go to plan")
        users = User.objects.all()
        for user in users:
            if Permission.objects.filter(package=package, user=user):
                user.has_permission = True
        context = {'users': users, 'package': package}
        return render(
            request,
            'package_permissions.html',
            context
        )
    else:
        package = Package.objects.get(pk=package_id)
        users = User.objects.all()
        for user in users:
            if Permission.objects.filter(package=package, user=user):
                user.has_permission = True
        context = {'users': users, 'package': package}
        return render(
            request,
            'package_permissions.html',
            context
        )


def cardsort_activity(request, package_id):
    """ Display the package for sorting, or save the sorted card arrangements and user comment on POST """
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
                sorted_group.title = request.POST['group_title_'+ str(sorted_group.pk)]
                group_text = request.POST['card_ids_for_' + str(sorted_group.pk)]
            else:
                group_text = request.POST['card_ids_for_' + str(group.pk)]
                group_title = request.POST['group_title_'+ str(group.pk)]
                sorted_group = SortedGroup(sorted_package=sorted_package,
                                           parent_group=group,
                                           title=group_title)
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

        messages.success(request, "Changes to " + package.name + " saved.")
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
    try:
        package = Package.objects.get(pk=package_id)
        temp_name = package.name
        package.delete()
        messages.success(request, "Package \'"+temp_name+"\' deleted successfully.")
    except KeyError:
        messages.error(request, "Sorry, something went wrong and we couldn't delete that package.")
    # except DatabaseError as e:
    #     messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
    #                    + e.__cause__ )
    #     print("ERROR: Database Error Deleting Package #" + package.id + "\n\r" + e.__cause__ )
    # except DataError as e:
    #     messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
    #                    + e.__cause__)
    #     print("ERROR: Data Error Deleting Package #" + package.id + "\n\r" + e.__cause__)
    # except IntegrityError as e:
    #     messages.error(request, "Sorry, something went wrong and we could not delete that package. ERROR:"
    #                    + e.__cause__ )
    #     print("ERROR: Integrity Error Deleting Package #" + package.id + "\n\r" + e.__cause__)

    own_packages = _admin_get_own_packages(request)
    context = {'own_packages': own_packages}
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


def _user_get_assigned_packages(request):
    """ Return a list of packages that have been assigned to the logged-in user """
    # filter the permissions to retrieve the permitted packages
    permissions = Permission.objects.filter(user=request.user)
    packages = []
    for permission in permissions:
        permitted_package = Package.objects.get(id=permission.package_id)
        packages.append(permitted_package)
    print(packages)
    return packages


def _admin_get_own_packages(request):
    """ Return a dict of packages owned by the logged-in admin """
    own_packages = Package.objects.filter(owner=request.user)
    return own_packages
