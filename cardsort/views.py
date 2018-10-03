from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from cardsort.forms import PackageForm
from cardsort.models import Package, UserSavedPackage, Card, AssignedPackage


def create_package(request):
    """ Administrator functionality to create new Packages with related Cards and Categories """
    if request.method == 'POST':
        form = PackageForm(request=request)
        if form.is_valid():
            form.save_data()
            messages.info(request, 'Save successful')
        else:
            messages.error(request, 'Package could not be saved - form not valid')  # send an error here as required
        return HttpResponseRedirect('administration')
    else:
        kwargs = {'num_categories': 3, 'num_cards': 3}
        form = PackageForm(**kwargs).to_dict()
        return render(
            request,
            'create_edit.html',
            context=form
        )


def edit_package(request, package_id):
    """ Display the editing page with pre-filled data; if POST, save the edited package and redirect to admin page """
    if request.method == 'POST':
        form = PackageForm(request=request)
        if form.is_valid():
            form.save_data()
            messages.info(request, 'Save successful')
        else:
            messages.error(request, "An error occurred when saving")
        return redirect('administration')
    else:
        filled_form = PackageForm(package_id=package_id).to_dict()
        return render(
            request,
            'create_edit.html',
            context=filled_form
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def package_administration(request):
    """ Generate and display the Administration page with a list of the packages the admin has created """
    own_packages = Package.objects.filter(owner=request.user, assignedpackage__isnull=True)
    context = {'own_packages': own_packages}
    return render(
        request,
        'package_administration.html',
        context
    )


def package_open(request, package_id):
    """ Display the package as a cardsort activity for the user to complete """
    if UserSavedPackage.objects.filter(base_package=package_id, user=request.user).exists():
        user_save = UserSavedPackage.objects.get(base_package=package_id, user=request.user)
        assigned_package = AssignedPackage.objects.get(pk=user_save.assigned_package.pk)
        context = assigned_package.to_dict()
        return render(
            request,
            'active.html',
            context
        )
    else:
        messages.error(request, "Sorry, this package is not assigned to this user")
        return render(
            request,
            'index.html',
        )


def activity_save(request, package_id):
    """ Save card > category associations and user comment in the database """
    if request.method == "POST":
        data = request.POST
        package = AssignedPackage.objects.get(pk=package_id)
        for category in package.get_categories():
            assigned_cards = data['card_ids_for_' + str(category.pk)].split(',')
            for card_id in assigned_cards:
                if not card_id == "":
                    card = Card.objects.get(pk=int(card_id))
                    card.category = category
                    card.save_data()
        user_save = UserSavedPackage.objects.get(assigned_package=package)
        package.comment_text = data['comment']
        package.save_data()
        user_save.save_data()
        messages.info(request, "Sort saved successfully!")
    return redirect('home')


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_choose_user(request, base_package_id):
    base_package = Package.objects.get(pk=base_package_id)
    user_list = User.objects.all()
    context = {'base_package': base_package,
               'user_list': user_list
               }
    return render(
        request,
        'assign_package.html',
        context
    )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def assign_package_to_user(request, base_package_id, user_id):
    """ Function to assign the active package to the provided user"""
    base_package = Package.objects.get(pk=base_package_id)
    assigned_user = User.objects.get(pk=user_id)
    if UserSavedPackage.objects.filter(base_package=base_package, user=assigned_user).exists():
        messages.info(request, "This package is already assigned to this user")
        return redirect('assign', base_package_id)
    else:
        # TODO Move to base_package.assign(user_id) and remove 'UserSavedPackage'
        # Duplicate the Package, Categories, and Cards, so they are for this user only
        new_package = base_package.assign()
        assignment = UserSavedPackage(base_package=base_package, assigned_package=new_package, user=assigned_user)
        assignment.save()
        messages.info(request, "Package successfully assigned to user")
        return redirect('assign', base_package_id)


@staff_member_required(None, redirect_field_name='next', login_url='login')
def delete_package(request, package_id):
    # TODO: try/catch errors here
    instance = Package.objects.get(pk=package_id)
    instance.delete()
    messages.info(request, "Package deleted")
    return redirect('administration')


def get_css(request, package_id):
    package = Package.objects.get(pk=package_id)
    main_color = package.main_color
    return render(
        request,
        'colors.css',
        {'main_color': main_color},
        content_type='text/css'
    )
