from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import RegistrationForm
from cardsort.forms import NewPackageForm, EditPackageForm, SubmittedForm
from cardsort.models import Package, UserSavedPackage, Category, AssignedPackage, Card


def index(request):
    """ View function for home page of site. """
    return render(
        request,
        'index.html',
    )


def register(request):
    """
    View to create a new user with data provided
    **Fails if the password does not meet the requirements, without advising the user of the reason**
    If successful, creates the user, logs them in and sends to home page;
    If fails, currently refreshes the page with no additional information
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
        else:
            messages.error("Form validation error")
            form = RegistrationForm()
            context = {'form': form}
            return render(
                request,
                'register.html',
                context
            )
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(
            request,
            'register.html',
            context
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def create_package(request):
    """ Administrator functionality to create new Packages with related Cards and Categories """
    if request.method == 'POST':
        form = SubmittedForm(request)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Package could not be saved')  # send an error her as required
        return HttpResponseRedirect('administration')
    else:
        form = NewPackageForm(2, 3).to_dict()
        return render(
            request,
            'create_edit.html',
            context=form
        )


@staff_member_required(None, redirect_field_name='next', login_url='login')
def edit_package(request, package_id):
    """ Display the editing page with pre-filled data; if POST, save the edited package and redirect to admin page """
    if request.method == 'POST':
        print(request.POST)
        form = SubmittedForm(request)
        if form.is_valid():
            form.save()
            messages.info(request, 'Changes saved.')
        else:
            messages.error(request, "An error occurred when saving")
        return redirect('administration')
    else:
        filled_form = EditPackageForm(package_id).to_dict()
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
                    card.save()
        user_save = UserSavedPackage.objects.get(assigned_package=package)
        package.comment_text = data['comment']
        package.save()
        user_save.save()
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
        # Duplicate the Package, Categories, and Cards, so they are for this user only
        new_package = base_package.assign()
        assignment = UserSavedPackage(base_package=base_package, assigned_package=new_package, user=assigned_user)
        assignment.save()
        messages.info(request, "Package successfully assigned to user")
        return redirect('assign', base_package_id)


@staff_member_required(None, redirect_field_name='next', login_url='login')
def delete_package(request, package_id):
    print("Got to here")
    # TODO: try/catch errors here
    instance = Package.objects.get(pk=package_id)
    instance.delete()
    messages.info(request, "Package deleted")
    return redirect('administration')
