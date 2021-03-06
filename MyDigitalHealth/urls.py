from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html', redirect_field_name='index.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register', views.register, name='register'),
    path('create_package', views.create_package, name='create'),
    path('active/<package_id>', views.cardsort_activity, name='active'),
    path('analysis/<package_id>/<user_id>', views.admin_analysis, name='analysis'),
    path('admin', views.package_administration, name='admin'),
    path('edit/<package_id>', views.edit_package, name='edit'),
    path('view/<package_id>', views.view_sorted_package, name='view'),
    path('permissions/<package_id>', views.package_permissions, name='permissions'),
    path('assign_package/<package_id>', views.assign_package, name='assign'),
    path('unassign_package/<package_id>', views.unassign_package, name='unassign'),
    path('delete/<package_id>', views.delete_package, name='delete'),
    path('css/<package_id>', views.get_css, name='css'),
    path('favicon.ico', RedirectView.as_view(url="/static/favicon.ico"))
]
